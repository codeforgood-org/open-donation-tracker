"""Campaign endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.campaign import Campaign
from app.models.organization import Organization
from app.schemas.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignResponse,
    CampaignProgress,
)

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
def create_campaign(
    campaign_data: CampaignCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new campaign"""
    # Verify organization exists and user owns it
    organization = db.query(Organization).filter(
        Organization.id == campaign_data.organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    if organization.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    campaign = Campaign(**campaign_data.model_dump())

    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    return campaign


@router.get("/", response_model=List[CampaignResponse])
def get_campaigns(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    organization_id: Optional[int] = None,
    active_only: bool = False,
    db: Session = Depends(get_db),
):
    """Get all campaigns"""
    query = db.query(Campaign)

    if organization_id:
        query = query.filter(Campaign.organization_id == organization_id)
    if active_only:
        query = query.filter(Campaign.is_active == True)

    campaigns = query.order_by(desc(Campaign.created_at)).offset(skip).limit(limit).all()
    return campaigns


@router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get a specific campaign"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    return campaign


@router.get("/{campaign_id}/progress", response_model=CampaignProgress)
def get_campaign_progress(campaign_id: int, db: Session = Depends(get_db)):
    """Get campaign progress"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    # Calculate progress
    percentage = (campaign.current_amount / campaign.goal_amount * 100) if campaign.goal_amount > 0 else 0
    donor_count = len(set(d.donor_id for d in campaign.donations))

    days_remaining = (campaign.end_date - datetime.utcnow()).days
    days_remaining = max(0, days_remaining)

    return CampaignProgress(
        campaign_id=campaign.id,
        name=campaign.name,
        goal_amount=campaign.goal_amount,
        current_amount=campaign.current_amount,
        percentage=round(percentage, 2),
        donor_count=donor_count,
        days_remaining=days_remaining,
        is_active=campaign.is_active,
    )


@router.patch("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(
    campaign_id: int,
    campaign_data: CampaignUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a campaign"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    # Check permissions
    organization = db.query(Organization).filter(Organization.id == campaign.organization_id).first()
    if organization.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Update fields
    for field, value in campaign_data.model_dump(exclude_unset=True).items():
        setattr(campaign, field, value)

    db.commit()
    db.refresh(campaign)

    return campaign


@router.delete("/{campaign_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_campaign(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a campaign"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()

    if not campaign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campaign not found",
        )

    # Check permissions
    organization = db.query(Organization).filter(Organization.id == campaign.organization_id).first()
    if organization.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    db.delete(campaign)
    db.commit()

    return None
