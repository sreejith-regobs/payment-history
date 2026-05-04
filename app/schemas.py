from __future__ import annotations
from decimal import Decimal
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.models import PaymentStatus


class PaymentCreate(BaseModel):
    user_id: str
    amount: Decimal = Field(gt=0, decimal_places=2)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    payment_method: str
    description: Optional[str] = None
    reference_id: Optional[str] = None


class PaymentUpdate(BaseModel):
    status: PaymentStatus


class PaymentResponse(BaseModel):
    id: UUID
    user_id: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    payment_method: str
    description: Optional[str]
    reference_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PaymentListResponse(BaseModel):
    total: int
    items: list[PaymentResponse]
