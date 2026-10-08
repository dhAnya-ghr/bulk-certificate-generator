from pathlib import Path
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


OUTPUT_DIR = Path("generated_certificates")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_certificate(
    recipient_name: str,
    event_name: str,
    certificate_title: str,
    certificate_id: int
) -> str:

    file_path = OUTPUT_DIR / f"certificate_{certificate_id}.pdf"

    page_width, page_height = landscape(A4)

    pdf = canvas.Canvas(str(file_path), pagesize=(page_width, page_height))

    # Border
    pdf.setLineWidth(3)
    pdf.rect(
        30,
        30,
        page_width - 60,
        page_height - 60
    )

    # Certificate title
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 120,
        certificate_title
    )

    # Main text
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 180,
        "This certificate is proudly presented to"
    )

    # Recipient name
    pdf.setFont("Helvetica-Bold", 30)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 240,
        recipient_name
    )

    # Event
    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(
        page_width / 2,
        page_height - 300,
        f"For participating in {event_name}"
    )

    # Certificate ID
    pdf.setFont("Helvetica", 10)
    pdf.drawCentredString(
        page_width / 2,
        70,
        f"Certificate ID: {certificate_id}"
    )

    pdf.save()

    return str(file_path)