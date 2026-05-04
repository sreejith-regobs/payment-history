from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PaymentCreate(BaseModel):
    user_id: str = Field(min_length=1, max_length=64)
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    status: str = Field(default="pending", max_length=32)
    method: str | None = Field(default=None, max_length=32)
    reference: str | None = Field(default=None, max_length=128)


class PaymentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    amount: Decimal
    currency: str
    status: str
    method: str | None
    reference: str | None
    created_at: datetime
