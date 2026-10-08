from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_job_status_and_certificate_retrieval():

    response = client.post(
        "/api/v1/certificates/jobs",
        json={
            "event_name": "Retrieval Test",
            "certificate_title": "Certificate of Participation",
            "recipients": [
                {
                    "name": "Retrieval User",
                    "email": "retrieval@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    job_id = response.json()["id"]

    status_response = client.get(
        f"/api/v1/certificates/jobs/{job_id}"
    )

    assert status_response.status_code == 200
    assert status_response.json()["status"] == "completed"

    certificates_response = client.get(
        f"/api/v1/certificates/jobs/{job_id}/certificates"
    )

    assert certificates_response.status_code == 200

    certificates = certificates_response.json()

    assert len(certificates) == 1
    assert certificates[0]["status"] == "completed"

    certificate_id = certificates[0]["id"]

    download_response = client.get(
        f"/api/v1/certificates/{certificate_id}"
    )

    assert download_response.status_code == 200
    assert download_response.headers["content-type"] == "application/pdf"