"""Donation endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.donation import Donation, DonationStatus
from app.models.organization import Organization
from app.models.campaign import Campaign
from app.schemas.donation import (
    DonationCreate,
    DonationUpdate,
    DonationResponse,
    DonationStats,
)

router = APIRouter(prefix="/donations", tags=["Donations"])


@router.post("/", response_model=DonationResponse, status_code=status.HTTP_201_CREATED)
def create_donation(
    donation_data: DonationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new donation"""
    # Verify organization exists
    organization = db.query(Organization).filter(
        Organization.id == donation_data.organization_id
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Verify campaign if provided
    if donation_data.campaign_id:
        campaign = db.query(Campaign).filter(
            Campaign.id == donation_data.campaign_id,
            Campaign.organization_id == donation_data.organization_id,
        ).first()
        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Campaign not found",
            )

    # Create donation
    donation = Donation(
        **donation_data.model_dump(),
        donor_id=current_user.id,
        status=DonationStatus.COMPLETED,
        transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
    )

    db.add(donation)

    # Update campaign amount if applicable
    if donation_data.campaign_id:
        campaign = db.query(Campaign).filter(Campaign.id == donation_data.campaign_id).first()
        campaign.current_amount += donation.amount

    db.commit()
    db.refresh(donation)

    return donation


@router.get("/", response_model=List[DonationResponse])
def get_donations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    organization_id: Optional[int] = None,
    campaign_id: Optional[int] = None,
    status: Optional[DonationStatus] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get donations (filtered by user's donations)"""
    query = db.query(Donation).filter(Donation.donor_id == current_user.id)

    if organization_id:
        query = query.filter(Donation.organization_id == organization_id)
    if campaign_id:
        query = query.filter(Donation.campaign_id == campaign_id)
    if status:
        query = query.filter(Donation.status == status)

    donations = query.order_by(desc(Donation.donation_date)).offset(skip).limit(limit).all()
    return donations


@router.get("/all", response_model=List[DonationResponse])
def get_all_donations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    organization_id: Optional[int] = None,
    campaign_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Get all donations (public, excluding anonymous donor info)"""
    query = db.query(Donation)

    if organization_id:
        query = query.filter(Donation.organization_id == organization_id)
    if campaign_id:
        query = query.filter(Donation.campaign_id == campaign_id)

    donations = query.order_by(desc(Donation.donation_date)).offset(skip).limit(limit).all()
    return donations


@router.get("/stats", response_model=DonationStats)
def get_donation_stats(
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Get donation statistics"""
    query = db.query(Donation)

    if organization_id:
        query = query.filter(Donation.organization_id == organization_id)

    donations = query.all()

    if not donations:
        return DonationStats(
            total_amount=0,
            donation_count=0,
            average_donation=0,
            largest_donation=0,
            by_status={},
            by_payment_method={},
        )

    total_amount = sum(d.amount for d in donations)
    donation_count = len(donations)
    average_donation = total_amount / donation_count if donation_count > 0 else 0
    largest_donation = max(d.amount for d in donations) if donations else 0

    by_status = {}
    for status in DonationStatus:
        count = sum(1 for d in donations if d.status == status)
        if count > 0:
            by_status[status.value] = count

    by_payment_method = {}
    for d in donations:
        if d.payment_method:
            method = d.payment_method.value
            by_payment_method[method] = by_payment_method.get(method, 0) + 1

    return DonationStats(
        total_amount=total_amount,
        donation_count=donation_count,
        average_donation=average_donation,
        largest_donation=largest_donation,
        by_status=by_status,
        by_payment_method=by_payment_method,
    )


@router.get("/{donation_id}", response_model=DonationResponse)
def get_donation(
    donation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific donation"""
    donation = db.query(Donation).filter(
        Donation.id == donation_id,
        Donation.donor_id == current_user.id,
    ).first()

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )

    return donation


@router.patch("/{donation_id}", response_model=DonationResponse)
def update_donation(
    donation_id: int,
    donation_data: DonationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a donation"""
    donation = db.query(Donation).filter(
        Donation.id == donation_id,
        Donation.donor_id == current_user.id,
    ).first()

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found",
        )

    # Update fields
    for field, value in donation_data.model_dump(exclude_unset=True).items():
        setattr(donation, field, value)

    db.commit()
    db.refresh(donation)

    return donation
