import asyncio
import time
import uuid
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.config import get_settings
from app.database import SessionLocal
from app.models import AuditLog
from app.security import decode_token


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app) -> None:
        super().__init__(app)
        self.settings = get_settings()
        self.requests: dict[str, deque[float]] = defaultdict(deque)
        self.lock = asyncio.Lock()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path in {"/health", "/docs", "/openapi.json"}:
            return await call_next(request)
        key = f"{request.client.host if request.client else 'unknown'}:{request.url.path}"
        now = time.monotonic()
        async with self.lock:
            events = self.requests[key]
            while events and now - events[0] > self.settings.rate_limit_window_seconds:
                events.popleft()
            if len(events) >= self.settings.rate_limit_requests:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"},
                    headers={"Retry-After": str(self.settings.rate_limit_window_seconds)},
                )
            events.append(now)
        return await call_next(request)


class AuditMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        actor = "anonymous"
        authorization = request.headers.get("Authorization", "")
        if authorization.startswith("Bearer "):
            try:
                actor = decode_token(authorization.removeprefix("Bearer ")).get("sub", "unknown")
            except Exception:
                actor = "invalid-token"
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        try:
            async with SessionLocal() as session:
                session.add(
                    AuditLog(
                        actor=actor,
                        action=request.method,
                        resource=request.url.path,
                        status_code=response.status_code,
                        ip_address=request.client.host if request.client else None,
                        request_id=request_id,
                    )
                )
                await session.commit()
        except Exception:
            # Logging must not leak database details or replace the API response.
            pass
        return response
