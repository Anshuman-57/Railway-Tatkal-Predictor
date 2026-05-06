
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.session import get_db
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.prediction_service import create_prediction
from app.models.domain import PredictionLog

router = APIRouter(prefix="/predictions", tags=["Predictions"])

@router.post("", response_model=PredictionResponse)
def predict(req: PredictionRequest, db: Session = Depends(get_db)):
    return create_prediction(req, db)

@router.get("/history")
def history(db: Session = Depends(get_db)):
    rows = db.query(PredictionLog).order_by(desc(PredictionLog.created_at)).limit(50).all()
    return [
        {
            "train_no": r.train_no,
            "route": f"{r.source}-{r.destination}",
            "class": r.travel_class,
            "wl": r.waitlist_position,
            "confirm": r.confirm_probability,
            "rac": r.rac_probability,
            "waiting": r.waiting_probability,
            "risk": r.risk_level,
            "created_at": str(r.created_at),
        } for r in rows
    ]
