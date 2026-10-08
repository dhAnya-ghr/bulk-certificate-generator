from fastapi import FastAPI

from app.database import Base, engine
from app.routers.certificates import router as certificate_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bulk Certificate Generator",
    description="Backend API for bulk certificate generation",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Bulk Certificate Generator API is running"
    }


app.include_router(certificate_router)