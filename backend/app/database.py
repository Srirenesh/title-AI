import logging
import os
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


settings = get_settings()
db_url = os.getenv("DATABASE_URL", str(settings.database_url))

engine_kwargs = {}
if "sqlite" in db_url:
    engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    engine_kwargs["pool_pre_ping"] = True
    engine_kwargs["pool_size"] = 10
    engine_kwargs["max_overflow"] = 20

_engine = create_async_engine(db_url, **engine_kwargs)
_session_factory = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)
engine = _engine


def _switch_to_sqlite():
    global _engine, _session_factory, engine
    fallback_url = "sqlite+aiosqlite:///./verity_title.db"
    logger.info("Falling back to local SQLite database: %s", fallback_url)
    _engine = create_async_engine(fallback_url, connect_args={"check_same_thread": False})
    engine = _engine
    _session_factory = async_sessionmaker(_engine, class_=AsyncSession, expire_on_commit=False)



def SessionLocal() -> AsyncSession:
    """Returns a new async session bound to the active database engine."""
    return _session_factory()


async def get_db() -> AsyncIterator[AsyncSession]:
    try:
        async with SessionLocal() as session:
            yield session
    except Exception as e:
        logger.warning("Database connection error: %s. Switching to SQLite fallback.", e)
        _switch_to_sqlite()
        async with SessionLocal() as session:
            yield session


async def init_db():
    global _engine
    try:
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        logger.warning("Primary DB connection refused (%s). Initializing fallback SQLite DB...", e)
        _switch_to_sqlite()
        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)



