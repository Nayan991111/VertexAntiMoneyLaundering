import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

class ReportService:
    def generate_sar_pdf(self, alert_id: str, ring_data: dict):
        """
        Generates a Suspicious Activity Report (SAR) in PDF format for Money Laundering Rings.
        Saves the file to the persistent /app/logs directory.
        """
        # Ensure directory exists
        log_dir = "/app/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        filename = f"SAR_{alert_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
        filepath = os.path.join(log_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # 1. HEADER
        title_style = styles['Title']
        story.append(Paragraph("CONFIDENTIAL - SUSPICIOUS ACTIVITY REPORT", title_style))
        story.append(Spacer(1, 12))
        
        # Meta Data
        story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Paragraph(f"<b>Case ID:</b> {alert_id}", styles['Normal']))
        story.append(Paragraph(f"<b>Filing Institution:</b> VertexAntiMoneyLaundering Algorithms Pvt Ltd", styles['Normal']))
        story.append(Spacer(1, 12))

        # 2. EXECUTIVE SUMMARY
        story.append(Paragraph("<b>Executive Summary:</b>", styles['Heading2']))
        summary_text = (
            "The VertexAntiMoneyLaundering Compliance Engine has detected a high-probability money laundering pattern "
            "involving circular funds transfer (Round Tripping). This activity indicates potential "
            "placement and layering stages of money laundering violations under the Bank Secrecy Act (BSA)."
        )
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 12))

        # 3. SUSPECT ENTITIES (The Ring)
        story.append(Paragraph("<b>Involved Entities (Ring Detected):</b>", styles['Heading2']))
        
        # Prepare Table Data
        # Header Row
        data = [["Sender", "Receiver", "Amount (USD)", "Risk Flag"]]
        
        # Extract Ring Data
        path_ids = ring_data.get('path_ids', [])
        amounts = ring_data.get('amounts', [])
        
        # Populate Rows
        for i in range(len(path_ids) - 1):
            sender = path_ids[i]
            receiver = path_ids[i+1]
            
            # Safe amount handling
            try:
                raw_amt = amounts[i] if i < len(amounts) else 0
                amt = f"${float(raw_amt):,.2f}"
            except:
                amt = "N/A"
                
            data.append([sender, receiver, amt, "High Velocity / Loop"])

        # Table Styling
        t = Table(data, colWidths=[150, 150, 100, 120])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(t)
        story.append(Spacer(1, 20))

        # 4. COMPLIANCE CERTIFICATION
        story.append(Paragraph("<b>Compliance Officer Certification:</b>", styles['Heading2']))
        cert_text = (
            "I hereby certify that the information contained in this report is true and accurate "
            "to the best of my knowledge. This report is filed in accordance with BSA/AML regulations."
        )
        story.append(Paragraph(cert_text, styles['Normal']))
        story.append(Spacer(1, 30))
        
        story.append(Paragraph("__________________________", styles['Normal']))
        story.append(Paragraph("Nayan (Sr. Compliance Architect)", styles['Normal']))
        story.append(Paragraph("VertexAntiMoneyLaundering Algorithms Pvt Ltd", styles['Normal']))

        # Build PDF
        doc.build(story)
        return filepath

# Export Singleton
report_service = ReportService()