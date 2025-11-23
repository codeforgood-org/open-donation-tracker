"""Impact report endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.impact import ImpactReport
from app.models.organization import Organization
from app.schemas.impact import (
    ImpactReportCreate,
    ImpactReportUpdate,
    ImpactReportResponse,
)

router = APIRouter(prefix="/impact-reports", tags=["Impact Reports"])


@router.post("/", response_model=ImpactReportResponse, status_code=status.HTTP_201_CREATED)
def create_impact_report(
    report_data: ImpactReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new impact report"""
    # Verify organization exists and user owns it
    organization = db.query(Organization).filter(
        Organization.id == report_data.organization_id
    ).first()

    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    if organization.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    report = ImpactReport(**report_data.model_dump())

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


@router.get("/", response_model=List[ImpactReportResponse])
def get_impact_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Get all impact reports"""
    query = db.query(ImpactReport)

    if organization_id:
        query = query.filter(ImpactReport.organization_id == organization_id)

    reports = query.order_by(desc(ImpactReport.created_at)).offset(skip).limit(limit).all()
    return reports


@router.get("/{report_id}", response_model=ImpactReportResponse)
def get_impact_report(report_id: int, db: Session = Depends(get_db)):
    """Get a specific impact report"""
    report = db.query(ImpactReport).filter(ImpactReport.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Impact report not found",
        )

    return report


@router.patch("/{report_id}", response_model=ImpactReportResponse)
def update_impact_report(
    report_id: int,
    report_data: ImpactReportUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an impact report"""
    report = db.query(ImpactReport).filter(ImpactReport.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Impact report not found",
        )

    # Check permissions
    organization = db.query(Organization).filter(Organization.id == report.organization_id).first()
    if organization.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    # Update fields
    for field, value in report_data.model_dump(exclude_unset=True).items():
        setattr(report, field, value)

    db.commit()
    db.refresh(report)

    return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_impact_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an impact report"""
    report = db.query(ImpactReport).filter(ImpactReport.id == report_id).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Impact report not found",
        )

    # Check permissions
    organization = db.query(Organization).filter(Organization.id == report.organization_id).first()
    if organization.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    db.delete(report)
    db.commit()

    return None
