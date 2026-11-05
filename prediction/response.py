from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HealthRiskPredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)   # ORM 객체 -> 응답 변환
    id: int
    user_id: int
    diabetes_probability: float
    hypertension_probability: float
    model_version: str
    created_at: datetime