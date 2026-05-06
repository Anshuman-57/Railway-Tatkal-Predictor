
from pydantic import BaseModel, Field
from typing import List, Dict

class PredictionRequest(BaseModel):
    train_no: str = Field(..., examples=["19483"])
    source: str = Field(..., examples=["ADI"])
    destination: str = Field(..., examples=["MFP"])
    travel_class: str = Field(..., examples=["3A"])
    quota: str = Field(default="GN", examples=["GN", "TQ", "PT"])
    waitlist_type: str = Field(default="GNWL", examples=["GNWL", "PQWL", "RLWL", "TQWL"])
    waitlist_position: int = Field(..., ge=1, le=500)
    days_before_journey: int = Field(..., ge=0, le=120)
    distance_km: int = Field(..., ge=1)
    journey_month: int = Field(..., ge=1, le=12)
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    is_festival_season: bool = False

class ProbabilityBreakdown(BaseModel):
    confirmed: float
    rac: float
    waiting: float

class Recommendation(BaseModel):
    title: str
    reason: str
    action: str

class PredictionResponse(BaseModel):
    probabilities: ProbabilityBreakdown
    risk_level: str
    confidence_score: float
    popularity_score: float
    expected_movement: int
    explanation: List[str]
    recommendations: List[Recommendation]
    similar_history: List[Dict]
