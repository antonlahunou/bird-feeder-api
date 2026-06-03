from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BirdBase(BaseModel):
    species: str
    confidence: Optional[float] = None
    photo_url: Optional[str] = None
    audio_url: Optional[str] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None

class BirdCreate(BirdBase):
    device_id: str
    detection_type: str  # 'audio' or 'video'

class BirdUpdate(BirdBase):
    pass

class BirdInDB(BirdBase):
    id: int
    device_id: str
    detection_type: str
    detected_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True