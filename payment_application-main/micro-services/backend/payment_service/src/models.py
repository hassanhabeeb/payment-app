# backend/payment_service/src/models.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentCreate(BaseModel):
    amount: float
    currency: str
    description: str
    payment_method: str

class Payment(PaymentCreate):
    id: str
    status: str
    created_at: datetime
    user_email: str