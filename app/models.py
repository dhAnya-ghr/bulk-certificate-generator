from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, default="pending")
    total = Column(Integer, default=0)
    completed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("generation_jobs.id"))
    recipient_name = Column(String, nullable=False)
    recipient_email = Column(String, nullable=False)
    status = Column(String, default="pending")
    file_path = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())