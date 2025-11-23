"""Export and reporting endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
import io

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.donation import Donation
from app.services.export import ExportService
from app.services.qrcode_service import QRCodeService

router = APIRouter(prefix="/export", tags=["Export"])


@router.get("/donations/csv")
def export_donations_csv(
    organization_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export user's donations to CSV"""
    query = db.query(Donation).filter(Donation.donor_id == current_user.id)

    if organization_id:
        query = query.filter(Donation.organization_id == organization_id)

    donations = query.all()

    # Convert to dict format
    donation_dicts = [
        {
            'id': d.id,
            'donation_date': d.donation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'amount': d.amount,
            'currency': d.currency,
            'status': d.status.value,
            'payment_method': d.payment_method.value if d.payment_method else '',
            'transaction_id': d.transaction_id,
            'organization_id': d.organization_id,
            'campaign_id': d.campaign_id or '',
        }
        for d in donations
    ]

    csv_content = ExportService.export_donations_csv(donation_dicts)

    return StreamingResponse(
        io.StringIO(csv_content),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=donations.csv"}
    )


@router.get("/donations/excel")
def export_donations_excel(
    organization_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export user's donations to Excel"""
    query = db.query(Donation).filter(Donation.donor_id == current_user.id)

    if organization_id:
        query = query.filter(Donation.organization_id == organization_id)

    donations = query.all()

    donation_dicts = [
        {
            'id': d.id,
            'donation_date': d.donation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'amount': d.amount,
            'currency': d.currency,
            'status': d.status.value,
            'payment_method': d.payment_method.value if d.payment_method else '',
            'transaction_id': d.transaction_id,
        }
        for d in donations
    ]

    excel_content = ExportService.export_donations_excel(donation_dicts)

    return Response(
        content=excel_content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=donations.xlsx"}
    )


@router.get("/donation/{donation_id}/receipt")
def get_donation_receipt(
    donation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate PDF receipt for a donation"""
    donation = db.query(Donation).filter(
        Donation.id == donation_id,
        Donation.donor_id == current_user.id
    ).first()

    if not donation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Donation not found"
        )

    receipt_data = {
        'donor_name': current_user.full_name,
        'donor_email': current_user.email,
        'amount': donation.amount,
        'currency': donation.currency,
        'transaction_id': donation.transaction_id,
        'donation_date': donation.donation_date.strftime('%B %d, %Y'),
        'payment_method': donation.payment_method.value if donation.payment_method else 'N/A',
        'organization_name': 'Organization',  # Would need to join with organization
        'campaign_name': 'Campaign' if donation.campaign_id else 'General Fund',
    }

    pdf_content = ExportService.generate_donation_receipt_pdf(receipt_data)

    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=receipt_{donation_id}.pdf"}
    )


@router.get("/campaign/{campaign_id}/qrcode")
def get_campaign_qr_code(campaign_id: int):
    """Generate QR code for campaign"""
    qr_code = QRCodeService.generate_campaign_qr(campaign_id)
    return {"qr_code": qr_code}


@router.get("/organization/{org_id}/qrcode")
def get_organization_qr_code(org_id: int):
    """Generate QR code for organization"""
    qr_code = QRCodeService.generate_organization_qr(org_id)
    return {"qr_code": qr_code}


@router.get("/donation-qr")
def get_donation_qr_code(
    campaign_id: int,
    organization_id: int,
    amount: Optional[float] = None
):
    """Generate QR code for quick donation"""
    qr_code = QRCodeService.generate_donation_qr(
        campaign_id=campaign_id,
        organization_id=organization_id,
        amount=amount
    )
    return {"qr_code": qr_code}
