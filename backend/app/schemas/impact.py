"""Impact report schemas"""
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field


class ImpactReportBase(BaseModel):
    """Base impact report schema"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    period_start: datetime
    period_end: datetime
    metrics: Dict = Field(default_factory=dict)
    report_url: Optional[str] = None
    images: List[str] = Field(default_factory=list)


class ImpactReportCreate(ImpactReportBase):
    """Impact report creation schema"""
    organization_id: int


class ImpactReportUpdate(BaseModel):
    """Impact report update schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    metrics: Optional[Dict] = None
    report_url: Optional[str] = None
    images: Optional[List[str]] = None


class ImpactReportResponse(ImpactReportBase):
    """Impact report response schema"""
    id: int
    organization_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
