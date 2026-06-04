from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BirdCreate(BaseModel):
    device_id: str
    detection_type: str
    species: str
    confidence: Optional[float] = None
    photo_url: Optional[str] = None
    audio_url: Optional[str] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None


class BirdResponse(BirdCreate):
    id: int
    detected_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True