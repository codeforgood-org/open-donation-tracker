"""Webhook management API"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
import secrets
import hmac
import hashlib
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.webhooks import Webhook, WebhookDelivery

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


class WebhookCreate(BaseModel):
    name: str
    url: HttpUrl
    events: List[str]  # donation_created, campaign_completed, etc.


class WebhookResponse(BaseModel):
    id: int
    name: str
    url: str
    events: List[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/", response_model=WebhookResponse)
def create_webhook(
    webhook_data: WebhookCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new webhook"""
    # Generate secret for HMAC verification
    secret = secrets.token_urlsafe(32)

    webhook = Webhook(
        **webhook_data.model_dump(),
        user_id=current_user.id,
        secret=secret
    )

    db.add(webhook)
    db.commit()
    db.refresh(webhook)

    return webhook


@router.get("/", response_model=List[WebhookResponse])
def list_webhooks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List user's webhooks"""
    webhooks = db.query(Webhook).filter(Webhook.user_id == current_user.id).all()
    return webhooks


@router.get("/{webhook_id}", response_model=WebhookResponse)
def get_webhook(
    webhook_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get webhook details"""
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id,
        Webhook.user_id == current_user.id
    ).first()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    return webhook


@router.delete("/{webhook_id}")
def delete_webhook(
    webhook_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a webhook"""
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id,
        Webhook.user_id == current_user.id
    ).first()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    db.delete(webhook)
    db.commit()

    return {"status": "success"}


@router.patch("/{webhook_id}/toggle")
def toggle_webhook(
    webhook_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle webhook active status"""
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id,
        Webhook.user_id == current_user.id
    ).first()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    webhook.is_active = not webhook.is_active
    db.commit()

    return {"id": webhook.id, "is_active": webhook.is_active}


@router.get("/{webhook_id}/deliveries")
def get_webhook_deliveries(
    webhook_id: int,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get webhook delivery history"""
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id,
        Webhook.user_id == current_user.id
    ).first()

    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    deliveries = db.query(WebhookDelivery).filter(
        WebhookDelivery.webhook_id == webhook_id
    ).order_by(WebhookDelivery.delivered_at.desc()).limit(limit).all()

    return [
        {
            "id": d.id,
            "event_type": d.event_type,
            "success": d.success,
            "status_code": d.status_code,
            "error_message": d.error_message,
            "delivered_at": d.delivered_at
        }
        for d in deliveries
    ]
