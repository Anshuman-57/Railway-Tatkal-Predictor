
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base, engine
from app.api.predictions import router as prediction_router
from app.api.analytics import router as analytics_router
from app.core.config import settings
import app.models.domain

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status":"ok", "service":settings.app_name}

app.include_router(prediction_router)
app.include_router(analytics_router)
