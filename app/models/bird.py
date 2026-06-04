from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.core.database import Base


class Bird(Base):
    __tablename__ = "birds"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, nullable=False)
    detection_type = Column(String, nullable=False)  # 'audio' or 'video'
    species = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    photo_url = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    location_lat = Column(Float, nullable=True)
    location_lon = Column(Float, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)