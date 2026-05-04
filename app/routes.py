from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .models import Payment
from .schemas import PaymentCreate, PaymentRead, PaymentStatus

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)) -> Payment:
    payment = Payment(
        user_id=payload.user_id,
        amount=payload.amount,
        currency=payload.currency.upper(),
        status=payload.status.value,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


@router.get("", response_model=list[PaymentRead])
def list_payments(
    user_id: Optional[str] = Query(default=None),
    status_filter: Optional[PaymentStatus] = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Payment]:
    stmt = select(Payment).order_by(Payment.created_at.desc())
    if user_id is not None:
        stmt = stmt.where(Payment.user_id == user_id)
    if status_filter is not None:
        stmt = stmt.where(Payment.status == status_filter.value)
    stmt = stmt.limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())


@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment(payment_id: UUID, db: Session = Depends(get_db)) -> Payment:
    payment = db.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="payment not found")
    return payment
