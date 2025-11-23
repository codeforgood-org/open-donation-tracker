"""Campaign schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CampaignBase(BaseModel):
    """Base campaign schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    goal_amount: float = Field(..., gt=0)
    currency: str = Field(default="USD", max_length=3)
    start_date: datetime
    end_date: datetime
    image_url: Optional[str] = None


class CampaignCreate(CampaignBase):
    """Campaign creation schema"""
    organization_id: int


class CampaignUpdate(BaseModel):
    """Campaign update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    goal_amount: Optional[float] = Field(None, gt=0)
    is_active: Optional[bool] = None
    end_date: Optional[datetime] = None
    image_url: Optional[str] = None


class CampaignResponse(CampaignBase):
    """Campaign response schema"""
    id: int
    current_amount: float
    is_active: bool
    organization_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CampaignProgress(BaseModel):
    """Campaign progress schema"""
    campaign_id: int
    name: str
    goal_amount: float
    current_amount: float
    percentage: float
    donor_count: int
    days_remaining: int
    is_active: bool
