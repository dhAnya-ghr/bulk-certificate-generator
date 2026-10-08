from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GenerationJob, Certificate
from app.schemas import CertificateJobCreate, JobResponse
from app.services.job_processor import process_job


router = APIRouter(
    prefix="/api/v1/certificates",
    tags=["Certificates"]
)


@router.post("/jobs", response_model=JobResponse)
def create_generation_job(
    request: CertificateJobCreate,
    db: Session = Depends(get_db)
):
    if not request.recipients:
        raise HTTPException(
            status_code=400,
            detail="At least one recipient is required"
        )

    job = GenerationJob(
        status="pending",
        total=len(request.recipients),
        completed=0,
        failed=0
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    for recipient in request.recipients:
        certificate = Certificate(
            job_id=job.id,
            recipient_name=recipient.name,
            recipient_email=recipient.email,
            status="pending"
        )

        db.add(certificate)

    db.commit()

    process_job(
        db=db,
        job=job,
        event_name=request.event_name,
        certificate_title=request.certificate_title
    )

    db.refresh(job)

    return job


@router.get("/jobs/{job_id}", response_model=JobResponse)
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(GenerationJob)
        .filter(GenerationJob.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found"
        )

    return job


@router.get("/jobs/{job_id}/certificates")
def get_job_certificates(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = (
        db.query(GenerationJob)
        .filter(GenerationJob.id == job_id)
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found"
        )

    certificates = (
        db.query(Certificate)
        .filter(Certificate.job_id == job_id)
        .all()
    )

    return certificates


@router.get("/{certificate_id}")
def download_certificate(
    certificate_id: int,
    db: Session = Depends(get_db)
):
    certificate = (
        db.query(Certificate)
        .filter(Certificate.id == certificate_id)
        .first()
    )

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    if certificate.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Certificate is not available"
        )

    return FileResponse(
        certificate.file_path,
        media_type="application/pdf",
        filename=f"certificate_{certificate.id}.pdf"
    )