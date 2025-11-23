"""Social features - comments, reviews, ratings"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    """Comments on campaigns or organizations"""

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    content = Column(Text, nullable=False)
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="comments")
    campaign = relationship("Campaign", backref="comments")
    organization = relationship("Organization", backref="comments")


class OrganizationReview(Base):
    """Reviews and ratings for organizations"""

    __tablename__ = "organization_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    rating = Column(Float, nullable=False)  # 1-5 stars
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    is_verified_donor = Column(Boolean, default=False)  # Has this user donated?
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="reviews")
    organization = relationship("Organization", backref="reviews")


class SocialShare(Base):
    """Track social media shares"""

    __tablename__ = "social_shares"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    platform = Column(String, nullable=False)  # facebook, twitter, linkedin, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="social_shares")
    campaign = relationship("Campaign", backref="social_shares")
    organization = relationship("Organization", backref="social_shares")


class ActivityFeed(Base):
    """Platform activity feed"""

    __tablename__ = "activity_feed"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    activity_type = Column(String, nullable=False)  # donation, comment, review, share, badge
    description = Column(Text, nullable=False)
    metadata = Column(Text, nullable=True)  # JSON data
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="activities")


class Notification(Base):
    """User notifications"""

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False)  # donation_receipt, campaign_update, badge_earned, etc.
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    link = Column(String, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", backref="notifications")
