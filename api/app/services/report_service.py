from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from app.models.threat import ThreatDecision

def generate_threat_report(threat: ThreatDecision) -> BytesIO:
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Shadowhawk Core - Threat Intelligence Report")
    
    # Content
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, height - 100, f"Title: {threat.title}")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 120, f"Threat ID: {threat.id}")
    p.drawString(100, height - 140, f"Risk Score: {threat.risk_score}")
    p.drawString(100, height - 160, f"Status: {threat.status}")
    p.drawString(100, height - 180, f"Created At: {threat.created_at}")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, height - 210, "Description:")
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 230, threat.description or "No description provided.")

    # Footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(100, 50, "Classified: Military-Grade Intelligence - For Internal Use Only")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
