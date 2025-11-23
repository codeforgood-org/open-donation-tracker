"""Organization endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin_user
from app.models.user import User
from app.models.organization import Organization
from app.models.donation import Donation
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationStats,
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
def create_organization(
    org_data: OrganizationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new organization"""
    # Check if EIN already exists
    if org_data.ein:
        existing_org = db.query(Organization).filter(Organization.ein == org_data.ein).first()
        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization with this EIN already exists",
            )

    organization = Organization(
        **org_data.model_dump(),
        owner_id=current_user.id,
    )

    db.add(organization)
    db.commit()
    db.refresh(organization)

    return organization


@router.get("/", response_model=List[OrganizationResponse])
def get_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    verified_only: bool = False,
    db: Session = Depends(get_db),
):
    """Get all organizations"""
    query = db.query(Organization)

    if category:
        query = query.filter(Organization.category == category)
    if verified_only:
        query = query.filter(Organization.is_verified == True)

    organizations = query.order_by(desc(Organization.transparency_score)).offset(skip).limit(limit).all()
    return organizations


@router.get("/{org_id}", response_model=OrganizationResponse)
def get_organization(org_id: int, db: Session = Depends(get_db)):
    """Get a specific organization"""
    organization = db.query(Organization).filter(Organization.id == org_id).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    return organization


@router.get("/{org_id}/stats", response_model=OrganizationStats)
def get_organization_stats(org_id: int, db: Session = Depends(get_db)):
    """Get organization statistics"""
    organization = db.query(Organization).filter(Organization.id == org_id).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Calculate stats
    donations = db.query(Donation).filter(Donation.organization_id == org_id).all()

    total_donations = sum(d.amount for d in donations)
    donation_count = len(donations)
    donor_count = len(set(d.donor_id for d in donations))

    active_campaigns = len([c for c in organization.campaigns if c.is_active])

    return OrganizationStats(
        total_donations=total_donations,
        donation_count=donation_count,
        donor_count=donor_count,
        active_campaigns=active_campaigns,
        transparency_score=organization.transparency_score,
    )


@router.patch("/{org_id}", response_model=OrganizationResponse)
def update_organization(
    org_id: int,
    org_data: OrganizationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an organization"""
    organization = db.query(Organization).filter(Organization.id == org_id).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Check permissions
    if organization.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Update fields
    for field, value in org_data.model_dump(exclude_unset=True).items():
        setattr(organization, field, value)

    db.commit()
    db.refresh(organization)

    return organization


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(
    org_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
):
    """Delete an organization (admin only)"""
    organization = db.query(Organization).filter(Organization.id == org_id).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    db.delete(organization)
    db.commit()

    return None
