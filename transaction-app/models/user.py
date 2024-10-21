from utils.db_connect import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Float, text, REAL 

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    
