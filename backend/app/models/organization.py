"""Organization model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organization(Base):
    """Organization/Charity model"""

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    website = Column(String)
    email = Column(String)
    phone = Column(String)
    ein = Column(String, unique=True, index=True)  # Employer Identification Number
    category = Column(String, index=True)  # e.g., "Education", "Healthcare", "Environment"
    logo_url = Column(String)
    is_verified = Column(Boolean, default=False)
    transparency_score = Column(Float, default=0.0)  # 0-100 score
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="organizations")
    donations = relationship("Donation", back_populates="organization", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="organization", cascade="all, delete-orphan")
    impact_reports = relationship("ImpactReport", back_populates="organization", cascade="all, delete-orphan")
