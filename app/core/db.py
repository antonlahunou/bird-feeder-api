from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from .config import settings

engine = create_async_engine(settings.database_url, echo=False, future=True)
SessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)

Base = declarative_base()

# Импортируем ВСЕ модели здесь, чтобы они зарегистрировались в Base.metadata
from app.models.bird import Bird  # noqa: F401, E402

async def init_db():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created.")