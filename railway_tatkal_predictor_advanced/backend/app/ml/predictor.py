
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from app.schemas.prediction import PredictionRequest
from app.ml.features import build_feature_vector, calculate_popularity

FEATURE_COLUMNS = ["wl_position", "days_before", "distance_km", "journey_month", "day_of_week", "festival", "wl_type_score", "class_demand", "quota_demand", "popularity"]

class TatkalPredictor:
    def __init__(self, model_path: str):
        self.model_path = Path(model_path)
        self.model = None
        if self.model_path.exists():
            self.model = joblib.load(self.model_path)

    def predict(self, req: PredictionRequest):
        features = build_feature_vector(req)
        X = pd.DataFrame([[features[c] for c in FEATURE_COLUMNS]], columns=FEATURE_COLUMNS)
        if self.model:
            probs = self.model.predict_proba(X)[0]
            classes = list(self.model.classes_)
            p = {c: float(probs[classes.index(c)]) if c in classes else 0.0 for c in ["CONFIRMED", "RAC", "WAITING"]}
        else:
            p = self._heuristic(req, features)
        popularity = calculate_popularity(req)
        confirmed = round(p["CONFIRMED"] * 100, 2)
        rac = round(p["RAC"] * 100, 2)
        waiting = round(p["WAITING"] * 100, 2)
        risk = "LOW" if confirmed >= 70 else "MEDIUM" if confirmed >= 40 or rac >= 35 else "HIGH"
        expected_movement = max(0, int((req.days_before_journey * 1.8) - (popularity * 0.12) + (30 / max(req.waitlist_position, 1))))
        confidence = min(95, max(55, 100 - abs(confirmed - waiting) * 0.3))
        return {
            "probabilities": {"confirmed": confirmed, "rac": rac, "waiting": waiting},
            "risk_level": risk,
            "confidence_score": round(confidence, 2),
            "popularity_score": popularity,
            "expected_movement": expected_movement,
            "explanation": self._explain(req, popularity, confirmed, rac, waiting),
            "recommendations": self._recommend(req, confirmed, rac, waiting),
            "similar_history": [
                {"train_no": req.train_no, "wl_start": max(1, req.waitlist_position-8), "final_status": "CONFIRMED", "days_before": req.days_before_journey+2},
                {"train_no": req.train_no, "wl_start": req.waitlist_position+5, "final_status": "RAC", "days_before": req.days_before_journey},
                {"train_no": req.train_no, "wl_start": req.waitlist_position+18, "final_status": "WAITING", "days_before": max(0, req.days_before_journey-1)},
            ]
        }

    def _heuristic(self, req, f):
        score = 0.72
        score -= req.waitlist_position * 0.012
        score += req.days_before_journey * 0.025
        score += f["wl_type_score"] * 0.16
        score -= f["quota_demand"] * 0.14
        score -= f["popularity"] * 0.004
        if req.is_festival_season: score -= 0.12
        confirmed = max(0.02, min(0.94, score))
        rac = max(0.03, min(0.45, 0.45 - abs(confirmed - 0.45) * 0.5))
        waiting = max(0.03, 1 - confirmed - rac)
        total = confirmed + rac + waiting
        return {"CONFIRMED": confirmed/total, "RAC": rac/total, "WAITING": waiting/total}

    def _explain(self, req, popularity, confirmed, rac, waiting):
        lines = []
        lines.append(f"Waitlist position {req.waitlist_position} and {req.days_before_journey} days remaining are the strongest factors.")
        lines.append(f"Route popularity score is {popularity}/100, so demand pressure is {'high' if popularity>75 else 'moderate' if popularity>55 else 'low'}.")
        if req.waitlist_type.upper() == "PQWL":
            lines.append("PQWL usually moves slower than GNWL because it is linked to pooled quota stations.")
        if req.quota.upper() in ["TQ", "PT"]:
            lines.append("Tatkal/Premium Tatkal has high demand and short cancellation window, so prediction uncertainty is higher.")
        return lines

    def _recommend(self, req, confirmed, rac, waiting):
        recs = []
        if confirmed < 45:
            recs.append({"title":"Search alternate route", "reason":"Confirmation probability is not strong.", "action":"Check nearby boarding stations or major junction routes."})
        if req.waitlist_type.upper() == "PQWL":
            recs.append({"title":"Prefer GNWL route", "reason":"GNWL generally has better movement than PQWL.", "action":"Try source from a train-originating station if practical."})
        if waiting > 45:
            recs.append({"title":"Keep backup booking", "reason":"Waiting probability is high.", "action":"Book bus/flight/alternate train as backup before prices rise."})
        if not recs:
            recs.append({"title":"Monitor after charting", "reason":"Chances look reasonable.", "action":"Track status before chart preparation and keep ID ready."})
        return recs
