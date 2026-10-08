from pathlib import Path

from app.services.certificate_generator import generate_certificate


def test_certificate_generation():

    file_path = generate_certificate(
        recipient_name="Test Recipient",
        event_name="Test Event",
        certificate_title="Certificate of Participation",
        certificate_id=9999
    )

    assert Path(file_path).exists()
    assert file_path.endswith(".pdf")

    Path(file_path).unlink()