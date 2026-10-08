from pydantic import BaseModel, EmailStr
from typing import List, Optional


class Recipient(BaseModel):
    name: str
    email: EmailStr


class CertificateJobCreate(BaseModel):
    event_name: str
    certificate_title: str
    recipients: List[Recipient]


class CertificateResponse(BaseModel):
    id: int
    recipient_name: str
    recipient_email: str
    status: str
    file_path: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class JobResponse(BaseModel):
    id: int
    status: str
    total: int
    completed: int
    failed: int

    class Config:
        from_attributes = True