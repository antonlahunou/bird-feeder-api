from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api.birds import router as birds_router
from .core.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown (можно оставить пустым или закрыть соединения)

app = FastAPI(title="Bird Feeder API", lifespan=lifespan)
app.include_router(birds_router)

@app.get("/health")
async def health():
    return {"status": "ok"}