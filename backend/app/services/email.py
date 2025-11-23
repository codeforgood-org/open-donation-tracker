"""Email service for notifications"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from typing import List, Optional
from app.core.config import settings


class EmailService:
    """Service for sending emails"""

    @staticmethod
    async def send_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ):
        """Send an email"""
        if not hasattr(settings, 'SMTP_HOST'):
            print(f"Email would be sent to {to_email}: {subject}")
            return  # Skip in development

        message = MIMEMultipart('alternative')
        message['From'] = settings.EMAIL_FROM
        message['To'] = to_email
        message['Subject'] = subject

        if text_content:
            message.attach(MIMEText(text_content, 'plain'))
        message.attach(MIMEText(html_content, 'html'))

        try:
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                use_tls=True,
            )
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            raise

    @staticmethod
    async def send_welcome_email(user_email: str, user_name: str):
        """Send welcome email to new user"""
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #0ea5e9; color: white; padding: 20px; text-align: center; }
                .content { background: #f9f9f9; padding: 30px; }
                .button { background: #0ea5e9; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
                .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to Open Donation Tracker!</h1>
                </div>
                <div class="content">
                    <h2>Hello {{ user_name }}!</h2>
                    <p>Thank you for joining our platform dedicated to transparent charitable giving.</p>
                    <p>You can now:</p>
                    <ul>
                        <li>Track all your donations in one place</li>
                        <li>Support verified organizations and campaigns</li>
                        <li>View detailed impact reports</li>
                        <li>Monitor your giving analytics</li>
                    </ul>
                    <a href="{{ app_url }}/dashboard" class="button">Go to Dashboard</a>
                    <p>If you have any questions, feel free to reach out to our support team.</p>
                </div>
                <div class="footer">
                    <p>© 2024 Open Donation Tracker. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """)

        html_content = template.render(
            user_name=user_name,
            app_url=settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:5173'
        )

        await EmailService.send_email(
            to_email=user_email,
            subject="Welcome to Open Donation Tracker!",
            html_content=html_content
        )

    @staticmethod
    async def send_donation_receipt(
        user_email: str,
        user_name: str,
        amount: float,
        currency: str,
        organization_name: str,
        transaction_id: str,
        donation_date: str
    ):
        """Send donation receipt email"""
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #10b981; color: white; padding: 20px; text-align: center; }
                .receipt { background: white; border: 2px solid #10b981; padding: 30px; margin: 20px 0; }
                .amount { font-size: 36px; font-weight: bold; color: #10b981; text-align: center; margin: 20px 0; }
                .details { background: #f9f9f9; padding: 20px; border-radius: 5px; }
                .detail-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #ddd; }
                .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Thank You for Your Donation!</h1>
                </div>
                <div class="receipt">
                    <h2>Donation Receipt</h2>
                    <div class="amount">{{ currency }} {{ amount }}</div>
                    <div class="details">
                        <div class="detail-row">
                            <span><strong>Donor:</strong></span>
                            <span>{{ user_name }}</span>
                        </div>
                        <div class="detail-row">
                            <span><strong>Organization:</strong></span>
                            <span>{{ organization_name }}</span>
                        </div>
                        <div class="detail-row">
                            <span><strong>Date:</strong></span>
                            <span>{{ donation_date }}</span>
                        </div>
                        <div class="detail-row">
                            <span><strong>Transaction ID:</strong></span>
                            <span>{{ transaction_id }}</span>
                        </div>
                    </div>
                    <p style="margin-top: 20px; text-align: center; color: #666;">
                        This email serves as your official donation receipt for tax purposes.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2024 Open Donation Tracker. All rights reserved.</p>
                    <p>Keep this receipt for your records.</p>
                </div>
            </div>
        </body>
        </html>
        """)

        html_content = template.render(
            user_name=user_name,
            amount=f"{amount:,.2f}",
            currency=currency,
            organization_name=organization_name,
            transaction_id=transaction_id,
            donation_date=donation_date
        )

        await EmailService.send_email(
            to_email=user_email,
            subject=f"Donation Receipt - {currency} {amount:,.2f}",
            html_content=html_content
        )

    @staticmethod
    async def send_campaign_update(
        user_email: str,
        user_name: str,
        campaign_name: str,
        update_message: str
    ):
        """Send campaign update notification"""
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #0ea5e9; color: white; padding: 20px; text-align: center; }
                .content { background: #f9f9f9; padding: 30px; }
                .update { background: white; padding: 20px; border-left: 4px solid #0ea5e9; margin: 20px 0; }
                .button { background: #0ea5e9; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
                .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Campaign Update</h1>
                </div>
                <div class="content">
                    <h2>Hello {{ user_name }}!</h2>
                    <p>There's an update on a campaign you've supported:</p>
                    <div class="update">
                        <h3>{{ campaign_name }}</h3>
                        <p>{{ update_message }}</p>
                    </div>
                    <a href="{{ app_url }}/campaigns" class="button">View Campaign</a>
                </div>
                <div class="footer">
                    <p>© 2024 Open Donation Tracker. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """)

        html_content = template.render(
            user_name=user_name,
            campaign_name=campaign_name,
            update_message=update_message,
            app_url=settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:5173'
        )

        await EmailService.send_email(
            to_email=user_email,
            subject=f"Campaign Update: {campaign_name}",
            html_content=html_content
        )

    @staticmethod
    async def send_impact_report_notification(
        user_email: str,
        user_name: str,
        organization_name: str,
        report_title: str
    ):
        """Send impact report notification"""
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #8b5cf6; color: white; padding: 20px; text-align: center; }
                .content { background: #f9f9f9; padding: 30px; }
                .highlight { background: white; padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center; }
                .button { background: #8b5cf6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0; }
                .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>New Impact Report Available</h1>
                </div>
                <div class="content">
                    <h2>Hello {{ user_name }}!</h2>
                    <p>{{ organization_name }} has published a new impact report:</p>
                    <div class="highlight">
                        <h3>{{ report_title }}</h3>
                        <p>See how your donations are making a difference!</p>
                    </div>
                    <a href="{{ app_url }}/impact" class="button">View Impact Report</a>
                </div>
                <div class="footer">
                    <p>© 2024 Open Donation Tracker. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """)

        html_content = template.render(
            user_name=user_name,
            organization_name=organization_name,
            report_title=report_title,
            app_url=settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:5173'
        )

        await EmailService.send_email(
            to_email=user_email,
            subject=f"New Impact Report: {report_title}",
            html_content=html_content
        )
