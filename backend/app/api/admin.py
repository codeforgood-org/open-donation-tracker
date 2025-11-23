"""Admin endpoints for platform management"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, extract
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.security import get_current_admin_user
from app.models.user import User
from app.models.organization import Organization
from app.models.donation import Donation, DonationStatus
from app.models.campaign import Campaign
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])


class PlatformStats(BaseModel):
    """Platform-wide statistics"""
    total_users: int
    active_users: int
    total_organizations: int
    verified_organizations: int
    total_campaigns: int
    active_campaigns: int
    total_donations: float
    donation_count: int
    donations_this_month: float
    donations_last_month: float
    growth_rate: float
    average_donation: float
    top_organizations: List[dict]
    recent_activity: List[dict]


class UserManagement(BaseModel):
    """User management data"""
    id: int
    email: str
    full_name: str
    is_active: bool
    is_admin: bool
    donation_count: int
    total_donated: float
    created_at: datetime


@router.get("/stats", response_model=PlatformStats)
def get_platform_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get platform-wide statistics (admin only)"""

    # User stats
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()

    # Organization stats
    total_orgs = db.query(Organization).count()
    verified_orgs = db.query(Organization).filter(Organization.is_verified == True).count()

    # Campaign stats
    total_campaigns = db.query(Campaign).count()
    active_campaigns = db.query(Campaign).filter(Campaign.is_active == True).count()

    # Donation stats
    all_donations = db.query(Donation).filter(Donation.status == DonationStatus.COMPLETED).all()
    total_donations = sum(d.amount for d in all_donations)
    donation_count = len(all_donations)
    average_donation = total_donations / donation_count if donation_count > 0 else 0

    # This month vs last month
    now = datetime.utcnow()
    first_day_this_month = datetime(now.year, now.month, 1)
    first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)

    donations_this_month = sum(
        d.amount for d in all_donations
        if d.donation_date >= first_day_this_month
    )
    donations_last_month = sum(
        d.amount for d in all_donations
        if first_day_last_month <= d.donation_date < first_day_this_month
    )

    growth_rate = 0
    if donations_last_month > 0:
        growth_rate = ((donations_this_month - donations_last_month) / donations_last_month) * 100

    # Top organizations by donations
    org_donations = db.query(
        Organization.id,
        Organization.name,
        func.sum(Donation.amount).label('total'),
        func.count(Donation.id).label('count')
    ).join(Donation).group_by(Organization.id, Organization.name)\
     .order_by(desc('total')).limit(5).all()

    top_organizations = [
        {
            "id": org.id,
            "name": org.name,
            "total_donations": float(org.total),
            "donation_count": org.count
        }
        for org in org_donations
    ]

    # Recent activity
    recent_donations = db.query(Donation)\
        .order_by(desc(Donation.created_at))\
        .limit(10).all()

    recent_activity = [
        {
            "type": "donation",
            "amount": d.amount,
            "currency": d.currency,
            "date": d.donation_date.isoformat(),
            "organization_id": d.organization_id
        }
        for d in recent_donations
    ]

    return PlatformStats(
        total_users=total_users,
        active_users=active_users,
        total_organizations=total_orgs,
        verified_organizations=verified_orgs,
        total_campaigns=total_campaigns,
        active_campaigns=active_campaigns,
        total_donations=total_donations,
        donation_count=donation_count,
        donations_this_month=donations_this_month,
        donations_last_month=donations_last_month,
        growth_rate=round(growth_rate, 2),
        average_donation=average_donation,
        top_organizations=top_organizations,
        recent_activity=recent_activity
    )


@router.get("/users", response_model=List[UserManagement])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get all users with donation statistics (admin only)"""

    users = db.query(User).offset(skip).limit(limit).all()

    result = []
    for user in users:
        donations = db.query(Donation).filter(Donation.donor_id == user.id).all()

        result.append(UserManagement(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_admin=user.is_admin,
            donation_count=len(donations),
            total_donated=sum(d.amount for d in donations),
            created_at=user.created_at
        ))

    return result


@router.patch("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Toggle user active status (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = not user.is_active
    db.commit()

    return {"id": user.id, "is_active": user.is_active}


@router.patch("/organizations/{org_id}/verify")
def verify_organization(
    org_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Verify an organization (admin only)"""
    org = db.query(Organization).filter(Organization.id == org_id).first()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )

    org.is_verified = True
    org.transparency_score = 95.0  # Set high score for verified orgs
    db.commit()

    return {"id": org.id, "is_verified": org.is_verified}


@router.get("/analytics/donations-by-month")
def get_donations_by_month(
    months: int = Query(12, ge=1, le=24),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get donation analytics by month (admin only)"""

    # Get donations for the last N months
    start_date = datetime.utcnow() - timedelta(days=months * 30)

    donations = db.query(
        func.date_trunc('month', Donation.donation_date).label('month'),
        func.sum(Donation.amount).label('total'),
        func.count(Donation.id).label('count')
    ).filter(
        Donation.donation_date >= start_date,
        Donation.status == DonationStatus.COMPLETED
    ).group_by('month').order_by('month').all()

    return [
        {
            "month": d.month.strftime('%Y-%m'),
            "total": float(d.total),
            "count": d.count
        }
        for d in donations
    ]


@router.get("/analytics/top-donors")
def get_top_donors(
    limit: int = Query(10, ge=1, le=100),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Get top donors by total donated (admin only)"""

    top_donors = db.query(
        User.id,
        User.full_name,
        User.email,
        func.sum(Donation.amount).label('total'),
        func.count(Donation.id).label('count')
    ).join(Donation).filter(
        Donation.status == DonationStatus.COMPLETED
    ).group_by(User.id, User.full_name, User.email)\
     .order_by(desc('total')).limit(limit).all()

    return [
        {
            "id": donor.id,
            "name": donor.full_name,
            "email": donor.email,
            "total_donated": float(donor.total),
            "donation_count": donor.count
        }
        for donor in top_donors
    ]


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete a user (admin only)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete admin users"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
