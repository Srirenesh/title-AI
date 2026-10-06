import hmac
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import Settings, get_settings

bearer = HTTPBearer(auto_error=True)


def create_access_token(subject: str, roles: list[str], settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "roles": roles,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expiration_minutes),
    }
    return jwt.encode(
        payload,
        settings.jwt_secret.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def authenticate_dev_user(username: str, password: str) -> bool:
    settings = get_settings()
    if settings.app_env == "production":
        return False
    return hmac.compare_digest(username, settings.dev_admin_username) and hmac.compare_digest(
        password, settings.dev_admin_password.get_secret_value()
    )


def decode_token(token: str) -> dict:
    settings = get_settings()
    try:
        return jwt.decode(
            token,
            settings.jwt_secret.get_secret_value(),
            algorithms=[settings.jwt_algorithm],
        )
    except jwt.PyJWTError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired bearer token",
        ) from error


async def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
) -> dict:
    return decode_token(credentials.credentials)


def require_roles(*allowed_roles: str):
    async def dependency(user: Annotated[dict, Depends(current_user)]) -> dict:
        if not set(user.get("roles", [])).intersection(allowed_roles):
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user

    return dependency


class CredentialCipher:
    """Encrypt provider credentials if they must be passed through internal boundaries."""

    def __init__(self, key: str | None = None) -> None:
        configured = key or (
            get_settings().credential_encryption_key.get_secret_value()
            if get_settings().credential_encryption_key
            else None
        )
        if not configured:
            raise RuntimeError("CREDENTIAL_ENCRYPTION_KEY is not configured")
        self._cipher = Fernet(configured.encode())

    def encrypt(self, value: str) -> str:
        return self._cipher.encrypt(value.encode()).decode()

    def decrypt(self, value: str) -> str:
        return self._cipher.decrypt(value.encode()).decode()
