
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.session import Base

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    train_no = Column(String, index=True)
    source = Column(String, index=True)
    destination = Column(String, index=True)
    travel_class = Column(String, index=True)
    quota = Column(String, index=True)
    waitlist_position = Column(Integer)
    days_before_journey = Column(Integer)
    popularity_score = Column(Float)
    confirm_probability = Column(Float)
    rac_probability = Column(Float)
    waiting_probability = Column(Float)
    risk_level = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AlertRule(Base):
    __tablename__ = "alert_rules"
    id = Column(Integer, primary_key=True, index=True)
    train_no = Column(String, index=True)
    target_probability = Column(Float)
    channel = Column(String, default="email")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
