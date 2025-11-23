"""Gamification endpoints"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.gamification import UserBadge, DonorLevel, Milestone
from app.services.gamification import GamificationService

router = APIRouter(prefix="/gamification", tags=["Gamification"])


class BadgeResponse(BaseModel):
    id: int
    badge_type: str
    description: str
    earned_at: datetime

    class Config:
        from_attributes = True


class DonorLevelResponse(BaseModel):
    level: str
    total_donated: float
    donation_count: int
    points: int
    rank: int | None

    class Config:
        from_attributes = True


class LeaderboardEntry(BaseModel):
    rank: int
    user_name: str
    level: str
    points: int
    total_donated: float


@router.get("/badges", response_model=List[BadgeResponse])
def get_my_badges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's badges"""
    badges = db.query(UserBadge).filter(UserBadge.user_id == current_user.id).all()
    return badges


@router.get("/level", response_model=DonorLevelResponse)
def get_my_level(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's donor level"""
    level = GamificationService.update_donor_level(current_user.id, db)
    return level


@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get global leaderboard"""
    levels = GamificationService.get_leaderboard(db, limit)

    result = []
    for level in levels:
        user = db.query(User).filter(User.id == level.user_id).first()
        if user:
            result.append(LeaderboardEntry(
                rank=level.rank or 0,
                user_name=user.full_name,
                level=level.level,
                points=level.points,
                total_donated=level.total_donated
            ))

    return result


@router.post("/check-achievements")
def check_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check and award new achievements"""
    new_badges = GamificationService.check_and_award_badges(current_user.id, db)
    updated_level = GamificationService.update_donor_level(current_user.id, db)

    return {
        "new_badges": len(new_badges),
        "badges": [{"type": b.badge_type, "description": b.description} for b in new_badges],
        "level": updated_level.level,
        "points": updated_level.points,
        "rank": updated_level.rank
    }


@router.get("/milestones/campaign/{campaign_id}")
def get_campaign_milestones(
    campaign_id: int,
    db: Session = Depends(get_db)
):
    """Get milestones for a campaign"""
    milestones = db.query(Milestone).filter(Milestone.campaign_id == campaign_id).all()

    return [
        {
            "id": m.id,
            "name": m.name,
            "description": m.description,
            "target_amount": m.target_amount,
            "achieved": m.achieved,
            "achieved_at": m.achieved_at
        }
        for m in milestones
    ]
