from utils.db_connect import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, text, REAL 

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    transaction_amount = Column(REAL, nullable=False)
    mob_no = Column(String, nullable=False)
    transaction_datetime = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'))
    pincode = Column(String)
