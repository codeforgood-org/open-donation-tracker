"""Social features API - comments, reviews, activity feed"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel, Field
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.social import Comment, OrganizationReview, SocialShare, ActivityFeed, Notification
from app.models.donation import Donation

router = APIRouter(prefix="/social", tags=["Social"])


# Schemas
class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    campaign_id: Optional[int] = None
    organization_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    rating: float = Field(..., ge=1, le=5)
    title: Optional[str] = None
    content: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    rating: float
    title: Optional[str]
    content: Optional[str]
    is_verified_donor: bool
    helpful_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationResponse(BaseModel):
    id: int
    type: str
    title: str
    message: str
    link: Optional[str]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Comments endpoints
@router.post("/comments", response_model=CommentResponse)
def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a comment on a campaign or organization"""
    comment = Comment(
        **comment_data.model_dump(),
        user_id=current_user.id
    )
    db.add(comment)

    # Create activity feed entry
    if comment_data.campaign_id:
        activity = ActivityFeed(
            user_id=current_user.id,
            activity_type="comment",
            description=f"{current_user.full_name} commented on a campaign",
            is_public=True
        )
        db.add(activity)

    db.commit()
    db.refresh(comment)

    return CommentResponse(
        id=comment.id,
        user_id=comment.user_id,
        user_name=current_user.full_name,
        content=comment.content,
        created_at=comment.created_at
    )


@router.get("/comments/campaign/{campaign_id}", response_model=List[CommentResponse])
def get_campaign_comments(
    campaign_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get comments for a campaign"""
    comments = db.query(Comment).filter(
        Comment.campaign_id == campaign_id,
        Comment.is_visible == True
    ).order_by(desc(Comment.created_at)).offset(skip).limit(limit).all()

    result = []
    for comment in comments:
        user = db.query(User).filter(User.id == comment.user_id).first()
        result.append(CommentResponse(
            id=comment.id,
            user_id=comment.user_id,
            user_name=user.full_name if user else "Anonymous",
            content=comment.content,
            created_at=comment.created_at
        ))

    return result


# Reviews endpoints
@router.post("/reviews/organization/{org_id}", response_model=ReviewResponse)
def create_review(
    org_id: int,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a review for an organization"""
    # Check if user has already reviewed
    existing = db.query(OrganizationReview).filter(
        OrganizationReview.user_id == current_user.id,
        OrganizationReview.organization_id == org_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this organization"
        )

    # Check if user has donated to this organization
    has_donated = db.query(Donation).filter(
        Donation.donor_id == current_user.id,
        Donation.organization_id == org_id
    ).first() is not None

    review = OrganizationReview(
        **review_data.model_dump(),
        user_id=current_user.id,
        organization_id=org_id,
        is_verified_donor=has_donated
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    return ReviewResponse(
        id=review.id,
        user_id=review.user_id,
        user_name=current_user.full_name,
        rating=review.rating,
        title=review.title,
        content=review.content,
        is_verified_donor=review.is_verified_donor,
        helpful_count=review.helpful_count,
        created_at=review.created_at
    )


@router.get("/reviews/organization/{org_id}", response_model=List[ReviewResponse])
def get_organization_reviews(
    org_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get reviews for an organization"""
    reviews = db.query(OrganizationReview).filter(
        OrganizationReview.organization_id == org_id
    ).order_by(desc(OrganizationReview.created_at)).offset(skip).limit(limit).all()

    result = []
    for review in reviews:
        user = db.query(User).filter(User.id == review.user_id).first()
        result.append(ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            user_name=user.full_name if user else "Anonymous",
            rating=review.rating,
            title=review.title,
            content=review.content,
            is_verified_donor=review.is_verified_donor,
            helpful_count=review.helpful_count,
            created_at=review.created_at
        ))

    return result


# Activity feed
@router.get("/activity-feed", response_model=List[dict])
def get_activity_feed(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get public activity feed"""
    activities = db.query(ActivityFeed).filter(
        ActivityFeed.is_public == True
    ).order_by(desc(ActivityFeed.created_at)).offset(skip).limit(limit).all()

    return [
        {
            "id": a.id,
            "activity_type": a.activity_type,
            "description": a.description,
            "created_at": a.created_at
        }
        for a in activities
    ]


# Notifications
@router.get("/notifications", response_model=List[NotificationResponse])
def get_my_notifications(
    unread_only: bool = False,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's notifications"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)

    if unread_only:
        query = query.filter(Notification.is_read == False)

    notifications = query.order_by(desc(Notification.created_at)).offset(skip).limit(limit).all()
    return notifications


@router.patch("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    db.commit()

    return {"status": "success"}


@router.post("/notifications/mark-all-read")
def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read"""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({"is_read": True})
    db.commit()

    return {"status": "success"}


@router.get("/notifications/unread-count")
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications"""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()

    return {"count": count}


# Social sharing tracking
@router.post("/share")
def track_social_share(
    campaign_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    platform: str = "twitter",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track a social media share"""
    share = SocialShare(
        user_id=current_user.id,
        campaign_id=campaign_id,
        organization_id=organization_id,
        platform=platform
    )
    db.add(share)
    db.commit()

    return {"status": "success"}
