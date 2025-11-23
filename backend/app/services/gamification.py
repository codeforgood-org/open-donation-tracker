"""Gamification service for badges and achievements"""
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.models.gamification import UserBadge, DonorLevel, BadgeType, Milestone
from app.models.user import User
from app.models.donation import Donation


class GamificationService:
    """Service for managing gamification features"""

    # Donor level thresholds
    LEVELS = {
        "Bronze": 0,
        "Silver": 500,
        "Gold": 1000,
        "Platinum": 5000,
        "Diamond": 10000,
    }

    @staticmethod
    def check_and_award_badges(user_id: int, db: Session) -> List[UserBadge]:
        """Check if user qualifies for any new badges"""
        new_badges = []

        # Get user's donations
        donations = db.query(Donation).filter(Donation.donor_id == user_id).all()
        total_donated = sum(d.amount for d in donations)
        donation_count = len(donations)

        # Check existing badges
        existing_badges = db.query(UserBadge).filter(UserBadge.user_id == user_id).all()
        earned_types = [b.badge_type for b in existing_badges]

        # First donation badge
        if BadgeType.FIRST_DONATION not in earned_types and donation_count >= 1:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.FIRST_DONATION,
                description="Made your first donation!"
            )
            db.add(badge)
            new_badges.append(badge)

        # Donation amount badges
        if BadgeType.BRONZE_DONOR not in earned_types and total_donated >= 100:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.BRONZE_DONOR,
                description="Donated $100 or more!"
            )
            db.add(badge)
            new_badges.append(badge)

        if BadgeType.SILVER_DONOR not in earned_types and total_donated >= 500:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.SILVER_DONOR,
                description="Donated $500 or more!"
            )
            db.add(badge)
            new_badges.append(badge)

        if BadgeType.GOLD_DONOR not in earned_types and total_donated >= 1000:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.GOLD_DONOR,
                description="Donated $1,000 or more!"
            )
            db.add(badge)
            new_badges.append(badge)

        if BadgeType.PLATINUM_DONOR not in earned_types and total_donated >= 5000:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.PLATINUM_DONOR,
                description="Donated $5,000 or more!"
            )
            db.add(badge)
            new_badges.append(badge)

        if BadgeType.DIAMOND_DONOR not in earned_types and total_donated >= 10000:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.DIAMOND_DONOR,
                description="Donated $10,000 or more!"
            )
            db.add(badge)
            new_badges.append(badge)

        # Donation count badges
        if BadgeType.SUPPORTER_10 not in earned_types and donation_count >= 10:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.SUPPORTER_10,
                description="Made 10+ donations!"
            )
            db.add(badge)
            new_badges.append(badge)

        if BadgeType.SUPPORTER_50 not in earned_types and donation_count >= 50:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.SUPPORTER_50,
                description="Made 50+ donations!"
            )
            db.add(badge)
            new_badges.append(badge)

        if BadgeType.SUPPORTER_100 not in earned_types and donation_count >= 100:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.SUPPORTER_100,
                description="Made 100+ donations!"
            )
            db.add(badge)
            new_badges.append(badge)

        # Check for recurring donations
        recurring_donations = [d for d in donations if d.is_recurring]
        if BadgeType.MONTHLY_GIVER not in earned_types and len(recurring_donations) > 0:
            badge = UserBadge(
                user_id=user_id,
                badge_type=BadgeType.MONTHLY_GIVER,
                description="Set up recurring donations!"
            )
            db.add(badge)
            new_badges.append(badge)

        db.commit()
        return new_badges

    @staticmethod
    def update_donor_level(user_id: int, db: Session) -> DonorLevel:
        """Update user's donor level based on total donations"""
        # Get or create donor level
        donor_level = db.query(DonorLevel).filter(DonorLevel.user_id == user_id).first()
        if not donor_level:
            donor_level = DonorLevel(user_id=user_id)
            db.add(donor_level)

        # Calculate total donated
        donations = db.query(Donation).filter(Donation.donor_id == user_id).all()
        total_donated = sum(d.amount for d in donations)
        donation_count = len(donations)

        # Update stats
        donor_level.total_donated = total_donated
        donor_level.donation_count = donation_count

        # Calculate points (1 point per dollar + bonus for count)
        donor_level.points = int(total_donated) + (donation_count * 10)

        # Determine level
        if total_donated >= GamificationService.LEVELS["Diamond"]:
            donor_level.level = "Diamond"
        elif total_donated >= GamificationService.LEVELS["Platinum"]:
            donor_level.level = "Platinum"
        elif total_donated >= GamificationService.LEVELS["Gold"]:
            donor_level.level = "Gold"
        elif total_donated >= GamificationService.LEVELS["Silver"]:
            donor_level.level = "Silver"
        else:
            donor_level.level = "Bronze"

        db.commit()
        db.refresh(donor_level)

        # Update global rankings
        GamificationService.update_rankings(db)

        return donor_level

    @staticmethod
    def update_rankings(db: Session):
        """Update global donor rankings"""
        # Get all donor levels ordered by points
        levels = db.query(DonorLevel).order_by(DonorLevel.points.desc()).all()

        for rank, level in enumerate(levels, 1):
            level.rank = rank

        db.commit()

    @staticmethod
    def get_leaderboard(db: Session, limit: int = 10) -> List[DonorLevel]:
        """Get top donors leaderboard"""
        return db.query(DonorLevel)\
            .order_by(DonorLevel.points.desc())\
            .limit(limit)\
            .all()

    @staticmethod
    def check_campaign_milestones(campaign_id: int, current_amount: float, db: Session):
        """Check and update campaign milestones"""
        milestones = db.query(Milestone).filter(
            Milestone.campaign_id == campaign_id,
            Milestone.achieved == False
        ).all()

        for milestone in milestones:
            if milestone.target_amount and current_amount >= milestone.target_amount:
                milestone.achieved = True
                milestone.achieved_at = datetime.utcnow()

        db.commit()
