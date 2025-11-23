"""QR Code generation service"""
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64


class QRCodeService:
    """Service for generating QR codes"""

    @staticmethod
    def generate_donation_qr(
        campaign_id: int,
        organization_id: int,
        amount: float = None,
        base_url: str = "http://localhost:5173"
    ) -> str:
        """Generate QR code for quick donation"""
        # Build donation URL
        url = f"{base_url}/campaigns/{campaign_id}/donate"
        if amount:
            url += f"?amount={amount}"

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"

    @staticmethod
    def generate_campaign_qr(campaign_id: int, base_url: str = "http://localhost:5173") -> str:
        """Generate QR code for campaign page"""
        url = f"{base_url}/campaigns/{campaign_id}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"

    @staticmethod
    def generate_organization_qr(org_id: int, base_url: str = "http://localhost:5173") -> str:
        """Generate QR code for organization page"""
        url = f"{base_url}/organizations/{org_id}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_str}"
