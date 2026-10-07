from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.config import get_settings
from app.database import Base, engine, init_db
from app.middleware import AuditMiddleware, RateLimitMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.auto_create_tables:
        await init_db()
    yield
    try:
        from app.database import engine
        await engine.dispose()
    except Exception:
        pass



app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description=(
        "Authorized-source Current Owner Search and Title Search pipeline. "
        "Results require examiner verification and are never represented as 100% accurate."
    ),
    lifespan=lifespan,
)
app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware)
app.include_router(router)


@app.get("/health", tags=["operations"])
async def health() -> dict[str, str]:
    return {"status": "ok", "source_mode": settings.source_mode}
