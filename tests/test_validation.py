from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_email():
    response = client.post(
        "/api/v1/certificates/jobs",
        json={
            "event_name": "Testing Workshop",
            "certificate_title": "Certificate of Participation",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422