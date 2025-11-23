"""Gamification system with badges and achievements"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class BadgeType(str, Enum):
    """Types of badges"""
    FIRST_DONATION = "first_donation"
    BRONZE_DONOR = "bronze_donor"  # $100+
    SILVER_DONOR = "silver_donor"  # $500+
    GOLD_DONOR = "gold_donor"  # $1000+
    PLATINUM_DONOR = "platinum_donor"  # $5000+
    DIAMOND_DONOR = "diamond_donor"  # $10000+
    MONTHLY_GIVER = "monthly_giver"
    SUPPORTER_10 = "supporter_10"  # 10+ donations
    SUPPORTER_50 = "supporter_50"  # 50+ donations
    SUPPORTER_100 = "supporter_100"  # 100+ donations
    CAMPAIGN_CHAMPION = "campaign_champion"  # Helped complete a campaign
    EARLY_ADOPTER = "early_adopter"
    GENEROUS_HEART = "generous_heart"  # Large single donation
    CONSISTENT_GIVER = "consistent_giver"  # 6 months of monthly donations
    IMPACT_SEEKER = "impact_seeker"  # Viewed 10+ impact reports
    COMMUNITY_BUILDER = "community_builder"  # Shared 5+ campaigns


class UserBadge(Base):
    """User badges and achievements"""

    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_type = Column(String, nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)
    description = Column(String)

    # Relationships
    user = relationship("User", backref="badges")


class DonorLevel(Base):
    """Track donor level progression"""

    __tablename__ = "donor_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    level = Column(String, default="Bronze")  # Bronze, Silver, Gold, Platinum, Diamond
    total_donated = Column(Float, default=0.0)
    donation_count = Column(Integer, default=0)
    points = Column(Integer, default=0)
    rank = Column(Integer, nullable=True)  # Global ranking
    streak_days = Column(Integer, default=0)  # Consecutive donation days
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="donor_level")


class Milestone(Base):
    """Track milestones (for campaigns or platform)"""

    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    type = Column(String, nullable=False)  # "campaign", "platform", "organization"
    name = Column(String, nullable=False)
    description = Column(String)
    target_amount = Column(Float, nullable=True)
    target_count = Column(Integer, nullable=True)
    achieved = Column(Boolean, default=False)
    achieved_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    campaign = relationship("Campaign", backref="milestones")
