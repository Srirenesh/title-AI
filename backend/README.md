# Verity COS & Title Search Backend

FastAPI and PostgreSQL pipeline for authorized Current Owner Search (COS), property-index
search, general-index search, deterministic record matching, and chain-of-title assembly.

This service is an examiner-assistance system. It does not make legal determinations, claim
complete coverage, or represent its output as 100% accurate.

## Source safety

- `SOURCE_MODE=mock` is the default.
- The mock mode recognizes only the documented development fixture:
  `123 Main Street`, `Travis County`, `TX`.
- Any other mock query returns `SOURCE_UNAVAILABLE`; it does not invent records.
- Authorized mode requires provider credentials and explicit provider implementations.
- Adapters must use authorized APIs, exports, feeds, or integrations. They must never bypass
  CAPTCHA, authentication, rate limits, or access controls.

## Run locally

```bash
cd backend
cp .env.example .env
# Replace JWT_SECRET and DEV_ADMIN_PASSWORD.
docker compose up --build
```

The API is available at `http://localhost:8000`, with OpenAPI docs at `/docs`.

For a host Python environment:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
uvicorn app.main:app --reload
```

## Authentication

Development and test environments expose `POST /api/auth/token`. Send:

```json
{"username": "admin", "password": "the DEV_ADMIN_PASSWORD value"}
```

Use the returned JWT as `Authorization: Bearer <token>`. The development token endpoint is
disabled in production. Production identity providers should issue compatible JWTs with
`sub` and `roles` claims. Search access requires `admin` or `examiner`.

## Example COS request

```bash
curl -X POST http://localhost:8000/api/cos/search \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Main Street",
    "county": "Travis County",
    "state": "TX",
    "owner_name": "John A Smith"
  }'
```

The response always includes `search_status`. Ambiguous or incomplete results return
`REVIEW_REQUIRED`; unavailable sources return `SOURCE_UNAVAILABLE`.

## API

- `POST /api/cos/search`
- `POST /api/pi/search`
- `POST /api/gi/search`
- `POST /api/chain-of-title/build`
- `GET /api/properties/{id}`
- `GET /api/properties/{id}/records`
- `GET /api/properties/{id}/chain`

## Production notes

- Set `AUTO_CREATE_TABLES=false` and manage schema changes through reviewed migrations.
- Store secrets in a managed secret store and rotate JWT/provider credentials.
- Set `CREDENTIAL_ENCRYPTION_KEY` to a Fernet key if credentials cross internal boundaries.
- Replace the in-process rate limiter with a shared Redis/gateway limiter when scaling to
  multiple API workers.
- Connect each adapter only after contractual authorization and provider-specific tests.
- Preserve raw source references for examiner review, retention, and audit requirements.
