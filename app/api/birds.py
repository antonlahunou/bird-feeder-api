from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import SessionLocal
from app.models.bird import Bird
from app.schemas.bird import BirdCreate, BirdInDB
from sqlalchemy import select

router = APIRouter(prefix="/birds", tags=["birds"])

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/", response_model=BirdInDB)
async def create_bird(bird: BirdCreate, db: AsyncSession = Depends(get_db)):
    new_bird = Bird(**bird.dict())
    db.add(new_bird)
    await db.commit()
    await db.refresh(new_bird)
    return new_bird

@router.get("/", response_model=list[BirdInDB])
async def list_birds(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Bird))
    return result.scalars().all()
