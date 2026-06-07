from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class BirdCreate(BaseModel):
    device_id: str = Field(..., min_length=1, max_length=100)
    detection_type: str
    species: str = Field(..., min_length=1, max_length=100)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    photo_url: Optional[str] = None
    audio_url: Optional[str] = None
    location_lat: Optional[float] = Field(None, ge=-90, le=90)
    location_lon: Optional[float] = Field(None, ge=-180, le=180)

    @field_validator("detection_type")
    @classmethod
    def validate_detection_type(cls, v: str) -> str:
        allowed = ["audio", "video"]
        if v not in allowed:
            raise ValueError(f"detection_type must be one of: {', '.join(allowed)}")
        return v

    @field_validator("device_id")
    @classmethod
    def validate_device_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("device_id cannot be empty")
        return v.strip()

    @field_validator("species")
    @classmethod
    def validate_species(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("species cannot be empty")
        return v.strip()


class BirdResponse(BirdCreate):
    id: int
    detected_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True