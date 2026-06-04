from fastapi import FastAPI
from app.api import router as birds_router
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bird Feeder API")

app.include_router(birds_router)


@app.get("/health")
def health():
    return {"status": "ok"}