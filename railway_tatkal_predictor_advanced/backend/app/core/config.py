
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Railway Tatkal Intelligence Platform"
    env: str = "development"
    database_url: str = "sqlite:///./tatkal.db"
    jwt_secret: str = "change-this-secret"
    access_token_expire_minutes: int = 120
    model_path: str = "app/ml/artifacts/tatkal_model.joblib"

    class Config:
        env_file = ".env"

settings = Settings()
