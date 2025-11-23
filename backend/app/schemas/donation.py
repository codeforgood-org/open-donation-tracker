"""Donation schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.donation import DonationStatus, PaymentMethod


class DonationBase(BaseModel):
    """Base donation schema"""
    amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None
    is_anonymous: bool = False
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None


class DonationCreate(DonationBase):
    """Donation creation schema"""
    organization_id: int
    campaign_id: Optional[int] = None


class DonationUpdate(BaseModel):
    """Donation update schema"""
    status: Optional[DonationStatus] = None
    notes: Optional[str] = None


class DonationResponse(DonationBase):
    """Donation response schema"""
    id: int
    status: DonationStatus
    transaction_id: Optional[str]
    donor_id: int
    organization_id: int
    campaign_id: Optional[int]
    donation_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class DonationStats(BaseModel):
    """Donation statistics schema"""
    total_amount: float
    donation_count: int
    average_donation: float
    largest_donation: float
    by_status: dict
    by_payment_method: dict
