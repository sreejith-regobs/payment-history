# payment-history

A FastAPI service for storing payment history records in PostgreSQL.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in real values
uvicorn app.main:app --reload
```

## Environment

Connection vars (synced from the DevLift-provisioned Postgres):

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DATABASE`

## Endpoints

- `POST /payments` — record a payment
- `GET /payments` — list (filter by `user_id`, `status`; paginate via `limit`, `offset`)
- `GET /payments/{id}` — fetch one
- `GET /health` — liveness
