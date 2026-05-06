
from sqlalchemy.orm import Session
from app.core.config import settings
from app.ml.predictor import TatkalPredictor
from app.models.domain import PredictionLog
from app.schemas.prediction import PredictionRequest

predictor = TatkalPredictor(settings.model_path)

def create_prediction(req: PredictionRequest, db: Session):
    result = predictor.predict(req)
    log = PredictionLog(
        train_no=req.train_no, source=req.source, destination=req.destination,
        travel_class=req.travel_class, quota=req.quota,
        waitlist_position=req.waitlist_position, days_before_journey=req.days_before_journey,
        popularity_score=result["popularity_score"], confirm_probability=result["probabilities"]["confirmed"],
        rac_probability=result["probabilities"]["rac"], waiting_probability=result["probabilities"]["waiting"],
        risk_level=result["risk_level"]
    )
    db.add(log)
    db.commit()
    return result
