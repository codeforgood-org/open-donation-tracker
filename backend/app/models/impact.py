"""Impact report model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class ImpactReport(Base):
    """Impact report model for tracking donation impact"""

    __tablename__ = "impact_reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)

    # Impact metrics (stored as JSON for flexibility)
    metrics = Column(JSON, default={})
    # Example: {"people_helped": 1000, "meals_provided": 5000, "trees_planted": 100}

    # Files/media
    report_url = Column(String)
    images = Column(JSON, default=[])

    # Foreign keys
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    organization = relationship("Organization", back_populates="impact_reports")
