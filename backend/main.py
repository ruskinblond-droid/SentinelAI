from fastapi import FastAPI

from backend.database.database import Base, engine
from backend.database import models

from backend.api.auth import router as auth_router
from backend.api.dashboard import router as dashboard_router
from backend.api.monitoring import router as monitoring_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SentinelAI API",
    description="AI-based continuous behavioral risk assessment system",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(monitoring_router)


@app.get("/")
def root():
    return {
        "message": "SentinelAI Backend is running",
        "status": "active"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

