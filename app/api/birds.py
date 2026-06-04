from http_exceptions import HTTPException
from fastapi import APIRouter, Depends, status
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


@router.post("/", response_model=BirdResponse, status_code=status.HTTP_201_CREATED)
def create_bird(bird: BirdCreate, db: Session = Depends(get_db)):
    db_bird = Bird(**bird.dict())
    db.add(db_bird)
    db.commit()
    db.refresh(db_bird)
    return db_bird


@router.get("/", response_model=list[BirdResponse])
def get_birds(db: Session = Depends(get_db)):
    return db.query(Bird).all()


@router.get("/{bird_id}", response_model=BirdResponse)
def get_bird(bird_id: int, db: Session = Depends(get_db)):
    bird = db.query(Bird).filter(Bird.id == bird_id).first()
    if not bird:
        raise HTTPException(status_code=404, detail=f"Bird with id {bird_id} not found")
    return bird


@router.put("/{bird_id}", response_model=BirdResponse)
def update_bird(bird_id: int, bird_data: BirdCreate, db: Session = Depends(get_db)):
    bird = db.query(Bird).filter(Bird.id == bird_id).first()
    if not bird:
        raise HTTPException(status_code=404, detail="Bird not found")

    exclude_fields = {"id", "created_at", "detected_at"}
    update_data = bird_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key not in exclude_fields:
            setattr(bird, key, value)

    db.commit()
    db.refresh(bird)
    return bird


@router.delete("/{bird_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bird(bird_id: int, db: Session = Depends(get_db)):
    bird = db.query(Bird).filter(Bird.id == bird_id).first()
    if not bird:
        raise HTTPException(status_code=404, detail=f"Bird with id {bird_id} not found")

    db.delete(bird)
    db.commit()
    return None