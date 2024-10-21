from pydantic import BaseModel
from datetime import datetime

# Pydantic model for the incoming transaction data
class TransactionCreate(BaseModel):
    customer_id: int
    transaction_amount: float
    mob_no: str
    transaction_datetime: datetime
    pincode: str
    class Config:
        from_attributes = True  # Use the new key instead of orm_mode

