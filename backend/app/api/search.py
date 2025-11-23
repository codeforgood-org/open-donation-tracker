"""Advanced search endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from pydantic import BaseModel

from app.core.database import get_db
from app.models.organization import Organization
from app.models.campaign import Campaign
from app.models.donation import Donation

router = APIRouter(prefix="/search", tags=["Search"])


class SearchResult(BaseModel):
    type: str  # "organization", "campaign"
    id: int
    name: str
    description: Optional[str]
    score: float  # Relevance score


@router.get("/", response_model=List[SearchResult])
def global_search(
    q: str = Query(..., min_length=2),
    category: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    verified_only: bool = False,
    active_only: bool = False,
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """Advanced global search across organizations and campaigns"""
    results = []

    # Search organizations
    org_query = db.query(Organization)

    # Text search
    search_term = f"%{q}%"
    org_query = org_query.filter(
        or_(
            Organization.name.ilike(search_term),
            Organization.description.ilike(search_term),
            Organization.category.ilike(search_term)
        )
    )

    if category:
        org_query = org_query.filter(Organization.category == category)

    if verified_only:
        org_query = org_query.filter(Organization.is_verified == True)

    orgs = org_query.limit(limit // 2).all()

    for org in orgs:
        # Calculate relevance score
        score = 1.0
        if org.name.lower().startswith(q.lower()):
            score = 2.0
        elif q.lower() in org.name.lower():
            score = 1.5

        results.append(SearchResult(
            type="organization",
            id=org.id,
            name=org.name,
            description=org.description,
            score=score
        ))

    # Search campaigns
    campaign_query = db.query(Campaign)

    campaign_query = campaign_query.filter(
        or_(
            Campaign.name.ilike(search_term),
            Campaign.description.ilike(search_term)
        )
    )

    if min_amount:
        campaign_query = campaign_query.filter(Campaign.goal_amount >= min_amount)

    if max_amount:
        campaign_query = campaign_query.filter(Campaign.goal_amount <= max_amount)

    if active_only:
        campaign_query = campaign_query.filter(Campaign.is_active == True)

    campaigns = campaign_query.limit(limit // 2).all()

    for campaign in campaigns:
        score = 1.0
        if campaign.name.lower().startswith(q.lower()):
            score = 2.0
        elif q.lower() in campaign.name.lower():
            score = 1.5

        results.append(SearchResult(
            type="campaign",
            id=campaign.id,
            name=campaign.name,
            description=campaign.description,
            score=score
        ))

    # Sort by relevance score
    results.sort(key=lambda x: x.score, reverse=True)

    return results[:limit]


@router.get("/organizations")
def search_organizations(
    q: str = Query(..., min_length=2),
    category: Optional[str] = None,
    min_transparency: Optional[float] = None,
    verified_only: bool = False,
    sort_by: str = "relevance",  # relevance, transparency, name
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """Advanced organization search with filters"""
    search_term = f"%{q}%"

    query = db.query(Organization).filter(
        or_(
            Organization.name.ilike(search_term),
            Organization.description.ilike(search_term),
            Organization.category.ilike(search_term),
            Organization.ein.ilike(search_term)
        )
    )

    if category:
        query = query.filter(Organization.category == category)

    if min_transparency:
        query = query.filter(Organization.transparency_score >= min_transparency)

    if verified_only:
        query = query.filter(Organization.is_verified == True)

    # Sorting
    if sort_by == "transparency":
        query = query.order_by(Organization.transparency_score.desc())
    elif sort_by == "name":
        query = query.order_by(Organization.name)

    organizations = query.limit(limit).all()

    return [
        {
            "id": org.id,
            "name": org.name,
            "description": org.description,
            "category": org.category,
            "transparency_score": org.transparency_score,
            "is_verified": org.is_verified
        }
        for org in organizations
    ]


@router.get("/campaigns")
def search_campaigns(
    q: str = Query(..., min_length=2),
    organization_id: Optional[int] = None,
    min_goal: Optional[float] = None,
    max_goal: Optional[float] = None,
    progress_min: Optional[float] = None,  # Minimum % funded
    progress_max: Optional[float] = None,  # Maximum % funded
    active_only: bool = False,
    sort_by: str = "relevance",  # relevance, progress, recent
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db)
):
    """Advanced campaign search with filters"""
    search_term = f"%{q}%"

    query = db.query(Campaign).filter(
        or_(
            Campaign.name.ilike(search_term),
            Campaign.description.ilike(search_term)
        )
    )

    if organization_id:
        query = query.filter(Campaign.organization_id == organization_id)

    if min_goal:
        query = query.filter(Campaign.goal_amount >= min_goal)

    if max_goal:
        query = query.filter(Campaign.goal_amount <= max_goal)

    if active_only:
        query = query.filter(Campaign.is_active == True)

    campaigns = query.limit(limit * 2).all()  # Get more to filter by progress

    # Filter by progress percentage
    if progress_min is not None or progress_max is not None:
        filtered = []
        for campaign in campaigns:
            progress = (campaign.current_amount / campaign.goal_amount * 100) if campaign.goal_amount > 0 else 0
            if progress_min and progress < progress_min:
                continue
            if progress_max and progress > progress_max:
                continue
            filtered.append(campaign)
        campaigns = filtered[:limit]

    # Sorting
    if sort_by == "progress":
        campaigns.sort(key=lambda c: (c.current_amount / c.goal_amount if c.goal_amount > 0 else 0), reverse=True)
    elif sort_by == "recent":
        campaigns.sort(key=lambda c: c.created_at, reverse=True)

    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "goal_amount": c.goal_amount,
            "current_amount": c.current_amount,
            "progress_percentage": (c.current_amount / c.goal_amount * 100) if c.goal_amount > 0 else 0,
            "is_active": c.is_active,
            "organization_id": c.organization_id
        }
        for c in campaigns[:limit]
    ]


@router.get("/autocomplete")
def autocomplete(
    q: str = Query(..., min_length=2),
    type: str = "all",  # all, organizations, campaigns
    limit: int = Query(10, le=20),
    db: Session = Depends(get_db)
):
    """Autocomplete suggestions for search"""
    results = []
    search_term = f"{q}%"  # Prefix match for autocomplete

    if type in ["all", "organizations"]:
        orgs = db.query(Organization.name).filter(
            Organization.name.ilike(search_term)
        ).limit(limit).all()
        results.extend([{"type": "organization", "name": org.name} for org in orgs])

    if type in ["all", "campaigns"]:
        campaigns = db.query(Campaign.name).filter(
            Campaign.name.ilike(search_term)
        ).limit(limit).all()
        results.extend([{"type": "campaign", "name": campaign.name} for campaign in campaigns])

    return results[:limit]
