"""Webhook system for third-party integrations"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Webhook(Base):
    """Webhook configuration"""

    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False)  # For HMAC verification
    events = Column(JSON, default=[])  # List of events to subscribe to
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", backref="webhooks")
    deliveries = relationship("WebhookDelivery", back_populates="webhook", cascade="all, delete-orphan")


class WebhookDelivery(Base):
    """Webhook delivery log"""

    __tablename__ = "webhook_deliveries"

    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, ForeignKey("webhooks.id"), nullable=False)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status_code = Column(Integer, nullable=True)
    response_body = Column(Text, nullable=True)
    success = Column(Boolean, default=False)
    error_message = Column(Text, nullable=True)
    delivered_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    webhook = relationship("Webhook", back_populates="deliveries")


class GiftDonation(Base):
    """Donations made as gifts to others"""

    __tablename__ = "gift_donations"

    id = Column(Integer, primary_key=True, index=True)
    donation_id = Column(Integer, ForeignKey("donations.id"), nullable=False, unique=True)
    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=True)
    gift_message = Column(Text, nullable=True)
    is_notified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    donation = relationship("Donation", backref="gift")


class DonationMatching(Base):
    """Corporate matching for donations"""

    __tablename__ = "donation_matching"

    id = Column(Integer, primary_key=True, index=True)
    donation_id = Column(Integer, ForeignKey("donations.id"), nullable=False)
    company_name = Column(String, nullable=False)
    match_amount = Column(Float, nullable=False)
    match_ratio = Column(Float, default=1.0)  # 1.0 = 100% match, 2.0 = 200% match
    status = Column(String, default="pending")  # pending, confirmed, paid
    confirmed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    donation = relationship("Donation", backref="matching")
