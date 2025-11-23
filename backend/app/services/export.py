"""Export service for generating reports"""
import csv
import io
from datetime import datetime
from typing import List
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch


class ExportService:
    """Service for exporting data in various formats"""

    @staticmethod
    def export_donations_csv(donations: List[dict]) -> str:
        """Export donations to CSV format"""
        output = io.StringIO()

        if not donations:
            return ""

        fieldnames = ['id', 'date', 'amount', 'currency', 'organization',
                     'campaign', 'status', 'payment_method', 'transaction_id']

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for donation in donations:
            writer.writerow({
                'id': donation.get('id', ''),
                'date': donation.get('donation_date', ''),
                'amount': donation.get('amount', ''),
                'currency': donation.get('currency', ''),
                'organization': donation.get('organization_name', ''),
                'campaign': donation.get('campaign_name', ''),
                'status': donation.get('status', ''),
                'payment_method': donation.get('payment_method', ''),
                'transaction_id': donation.get('transaction_id', ''),
            })

        return output.getvalue()

    @staticmethod
    def export_donations_excel(donations: List[dict]) -> bytes:
        """Export donations to Excel format"""
        df = pd.DataFrame(donations)

        # Select and rename columns
        columns = {
            'id': 'ID',
            'donation_date': 'Date',
            'amount': 'Amount',
            'currency': 'Currency',
            'organization_name': 'Organization',
            'campaign_name': 'Campaign',
            'status': 'Status',
            'payment_method': 'Payment Method',
            'transaction_id': 'Transaction ID'
        }

        df = df[[col for col in columns.keys() if col in df.columns]]
        df.rename(columns=columns, inplace=True)

        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Donations', index=False)

            # Auto-adjust column widths
            worksheet = writer.sheets['Donations']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        return output.getvalue()

    @staticmethod
    def generate_donation_receipt_pdf(donation_data: dict) -> bytes:
        """Generate a PDF receipt for a donation"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0ea5e9'),
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("DONATION RECEIPT", title_style))
        story.append(Spacer(1, 0.5*inch))

        # Thank you message
        story.append(Paragraph(
            "Thank you for your generous donation!",
            styles['Heading2']
        ))
        story.append(Spacer(1, 0.3*inch))

        # Receipt details table
        data = [
            ['Receipt Date:', datetime.now().strftime('%B %d, %Y')],
            ['Transaction ID:', donation_data.get('transaction_id', 'N/A')],
            ['', ''],
            ['Donor Name:', donation_data.get('donor_name', '')],
            ['Donor Email:', donation_data.get('donor_email', '')],
            ['', ''],
            ['Organization:', donation_data.get('organization_name', '')],
            ['Campaign:', donation_data.get('campaign_name', 'General Fund')],
            ['', ''],
            ['Donation Amount:', f"{donation_data.get('currency', 'USD')} {donation_data.get('amount', 0):,.2f}"],
            ['Payment Method:', donation_data.get('payment_method', '').replace('_', ' ').title()],
            ['Donation Date:', donation_data.get('donation_date', '')],
        ]

        table = Table(data, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('LINEBELOW', (0, 8), (-1, 8), 2, colors.HexColor('#0ea5e9')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))

        story.append(table)
        story.append(Spacer(1, 0.5*inch))

        # Tax deductible notice
        story.append(Paragraph(
            "<b>Important Tax Information:</b> This receipt serves as official documentation "
            "of your charitable contribution. Please keep this receipt for your tax records. "
            "Consult with your tax advisor for specific deduction eligibility.",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.3*inch))

        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(
            "Open Donation Tracker | Ensuring Transparency in Charitable Giving",
            footer_style
        ))

        # Build PDF
        doc.build(story)
        return buffer.getvalue()

    @staticmethod
    def generate_impact_report_pdf(report_data: dict) -> bytes:
        """Generate a PDF impact report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        styles = getSampleStyleSheet()

        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=colors.HexColor('#8b5cf6'),
            spaceAfter=20,
            alignment=1
        )
        story.append(Paragraph("IMPACT REPORT", title_style))
        story.append(Paragraph(
            report_data.get('title', 'Quarterly Impact Report'),
            styles['Heading2']
        ))
        story.append(Spacer(1, 0.3*inch))

        # Organization info
        story.append(Paragraph(
            f"<b>Organization:</b> {report_data.get('organization_name', '')}",
            styles['Normal']
        ))
        story.append(Paragraph(
            f"<b>Report Period:</b> {report_data.get('period_start', '')} to {report_data.get('period_end', '')}",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.3*inch))

        # Description
        if report_data.get('description'):
            story.append(Paragraph("<b>Summary</b>", styles['Heading3']))
            story.append(Paragraph(report_data['description'], styles['Normal']))
            story.append(Spacer(1, 0.2*inch))

        # Metrics
        if report_data.get('metrics'):
            story.append(Paragraph("<b>Impact Metrics</b>", styles['Heading3']))

            metrics_data = [['Metric', 'Value']]
            for key, value in report_data['metrics'].items():
                metrics_data.append([
                    key.replace('_', ' ').title(),
                    str(value)
                ])

            metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
            metrics_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))

            story.append(metrics_table)

        # Build PDF
        doc.build(story)
        return buffer.getvalue()
