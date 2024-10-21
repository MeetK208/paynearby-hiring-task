from pydantic import BaseModel
from datetime import datetime

# Pydantic model for the incoming transaction data
class UserCreate(BaseModel):
    name: str
    state: str
    
    class Config:
        from_attributes = True  # Use the new key instead of orm_mode