from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_generation_job():
    response = client.post(
        "/api/v1/certificates/jobs",
        json={
            "event_name": "Testing Workshop",
            "certificate_title": "Certificate of Participation",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert data["total"] == 1
    assert data["completed"] == 1
    assert data["failed"] == 0


def test_individual_certificate_failure_does_not_stop_job(monkeypatch):
    from app.services import job_processor

    original_generate = job_processor.generate_certificate

    call_count = 0

    def failing_generator(
        recipient_name,
        event_name,
        certificate_title,
        certificate_id
    ):
        nonlocal call_count

        call_count += 1

        if call_count == 1:
            raise Exception("Simulated certificate generation failure")

        return original_generate(
            recipient_name,
            event_name,
            certificate_title,
            certificate_id
        )

    monkeypatch.setattr(
        job_processor,
        "generate_certificate",
        failing_generator
    )

    response = client.post(
        "/api/v1/certificates/jobs",
        json={
            "event_name": "Failure Test Workshop",
            "certificate_title": "Certificate of Participation",
            "recipients": [
                {
                    "name": "Failed User",
                    "email": "failed@example.com"
                },
                {
                    "name": "Successful User",
                    "email": "success@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert data["completed"] == 1
    assert data["failed"] == 1
    assert data["status"] == "completed_with_errors"