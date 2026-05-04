from fastapi import FastAPI

from .database import Base, engine
from .routes import router as payments_router

app = FastAPI(title="Payment History Service", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(payments_router)
