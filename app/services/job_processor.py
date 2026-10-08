from sqlalchemy.orm import Session

from app.models import GenerationJob, Certificate
from app.services.certificate_generator import generate_certificate


def process_job(
    db: Session,
    job: GenerationJob,
    event_name: str,
    certificate_title: str
):
    job.status = "processing"
    db.commit()

    certificates = (
        db.query(Certificate)
        .filter(Certificate.job_id == job.id)
        .all()
    )

    for certificate in certificates:

        try:
            file_path = generate_certificate(
                recipient_name=certificate.recipient_name,
                event_name=event_name,
                certificate_title=certificate_title,
                certificate_id=certificate.id
            )

            certificate.status = "completed"
            certificate.file_path = file_path

            job.completed += 1

        except Exception as error:

            certificate.status = "failed"
            certificate.error_message = str(error)

            job.failed += 1

        db.commit()

    if job.failed == 0:
        job.status = "completed"
    elif job.completed > 0:
        job.status = "completed_with_errors"
    else:
        job.status = "failed"

    db.commit()