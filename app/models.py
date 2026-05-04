import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Numeric, DateTime, Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
import enum
from app.database import Base


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False, index=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    status = Column(SAEnum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    payment_method = Column(String, nullable=False)
    description = Column(String, nullable=True)
    reference_id = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))
