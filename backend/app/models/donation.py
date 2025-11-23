"""Donation model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class DonationStatus(str, enum.Enum):
    """Donation status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"
    FAILED = "failed"


class PaymentMethod(str, enum.Enum):
    """Payment method enumeration"""
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    PAYPAL = "paypal"
    CRYPTO = "crypto"
    CASH = "cash"
    CHECK = "check"


class Donation(Base):
    """Donation model"""

    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    status = Column(Enum(DonationStatus), default=DonationStatus.PENDING, index=True)
    payment_method = Column(Enum(PaymentMethod))
    transaction_id = Column(String, unique=True, index=True)
    notes = Column(Text)
    is_anonymous = Column(Integer, default=False)
    is_recurring = Column(Integer, default=False)
    recurring_frequency = Column(String)  # "monthly", "quarterly", "yearly"

    # Foreign keys
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=True)

    # Timestamps
    donation_date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    donor = relationship("User", back_populates="donations")
    organization = relationship("Organization", back_populates="donations")
    campaign = relationship("Campaign", back_populates="donations")
