from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.bird import Bird
from app.schemas.bird import BirdCreate, BirdResponse

router = APIRouter(prefix="/birds", tags=["birds"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=BirdResponse)
def create_bird(bird: BirdCreate, db: Session = Depends(get_db)):
    db_bird = Bird(**bird.dict())
    db.add(db_bird)
    db.commit()
    db.refresh(db_bird)
    return db_bird


@router.get("/", response_model=list[BirdResponse])
def get_birds(db: Session = Depends(get_db)):
    return db.query(Bird).all()