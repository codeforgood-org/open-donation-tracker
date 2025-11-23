"""Organization schemas"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, HttpUrl


class OrganizationBase(BaseModel):
    """Base organization schema"""
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    website: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    ein: Optional[str] = None
    category: Optional[str] = None
    logo_url: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    """Organization creation schema"""
    pass


class OrganizationUpdate(BaseModel):
    """Organization update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    website: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    category: Optional[str] = None
    logo_url: Optional[str] = None


class OrganizationResponse(OrganizationBase):
    """Organization response schema"""
    id: int
    is_verified: bool
    transparency_score: float
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrganizationStats(BaseModel):
    """Organization statistics schema"""
    total_donations: float
    donation_count: int
    donor_count: int
    active_campaigns: int
    transparency_score: float
