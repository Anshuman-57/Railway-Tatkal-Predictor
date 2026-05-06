
import math
from app.schemas.prediction import PredictionRequest

WAITLIST_TYPE_SCORE = {"GNWL": 1.0, "RLWL": 0.75, "PQWL": 0.45, "TQWL": 0.35}
CLASS_DEMAND = {"SL": 0.72, "3E": 0.78, "3A": 0.85, "2A": 0.8, "1A": 0.65, "CC": 0.7}
QUOTA_DEMAND = {"GN": 0.75, "TQ": 0.92, "PT": 0.95}

def calculate_popularity(req: PredictionRequest) -> float:
    base = 55
    if req.distance_km > 900:
        base += 12
    if req.travel_class in ["3A", "SL"]:
        base += 10
    if req.quota in ["TQ", "PT"]:
        base += 15
    if req.is_festival_season:
        base += 18
    if req.day_of_week in [4, 5, 6]:
        base += 8
    seasonal = 6 * math.sin((req.journey_month / 12) * 2 * math.pi)
    return round(max(0, min(100, base + seasonal)), 2)

def build_feature_vector(req: PredictionRequest):
    popularity = calculate_popularity(req)
    return {
        "wl_position": req.waitlist_position,
        "days_before": req.days_before_journey,
        "distance_km": req.distance_km,
        "journey_month": req.journey_month,
        "day_of_week": req.day_of_week,
        "festival": int(req.is_festival_season),
        "wl_type_score": WAITLIST_TYPE_SCORE.get(req.waitlist_type.upper(), 0.5),
        "class_demand": CLASS_DEMAND.get(req.travel_class.upper(), 0.75),
        "quota_demand": QUOTA_DEMAND.get(req.quota.upper(), 0.8),
        "popularity": popularity,
    }
