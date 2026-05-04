from typing import Optional
from uuid import UUID
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db, engine, Base
from app.models import Payment, PaymentStatus
from app.schemas import PaymentCreate, PaymentUpdate, PaymentResponse, PaymentListResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payment History Service", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/payments", response_model=PaymentResponse, status_code=201)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    payment = Payment(**payload.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@app.get("/payments", response_model=PaymentListResponse)
def list_payments(
    user_id: Optional[str] = Query(None),
    status: Optional[PaymentStatus] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(Payment)
    if user_id:
        q = q.filter(Payment.user_id == user_id)
    if status:
        q = q.filter(Payment.status == status)
    total = q.with_entities(func.count()).scalar()
    items = q.order_by(Payment.created_at.desc()).offset(offset).limit(limit).all()
    return {"total": total, "items": items}


@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: UUID, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@app.patch("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment_status(payment_id: UUID, payload: PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    payment.status = payload.status
    db.commit()
    db.refresh(payment)
    return payment
