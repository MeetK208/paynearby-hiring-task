from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.transactionDb import Transaction as TransactionModel, Base  # Your SQLAlchemy model
from utils.db_connect import SessionLocal  # Import your session local
from datetime import datetime
from utils.schema import TransactionCreate
from utils.db_connect import engine, SessionLocal
from routes import transaction_router, user_routes

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tests.run_query import execute_query  ## To start FastAPI Server

# print(execute_query("DELETE FROM \"transaction\" WHERE pincode = 'string'"))
app = FastAPI()

# To Create Table if not exist
Base.metadata.create_all(bind = engine) 

# Routes Include

# Dependency to get the database session
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield the session
    finally:
        db.close()  # Close the session when done

# To Work With Transaction releted Data
app.include_router(transaction_router.router, prefix="/transaction")

# To Work with User Data - To get Name & State
app.include_router(user_routes.router, prefix="/register")


@app.get("/")
async def user_transaction_by_state():
    about_me_data = {
        "name": "Meet Kothari",
        "education": "Pursuing post-graduation at the Dhirubhai Ambani Institute of Information and Communication Technology",
        "about": "With a strong background in data engineering, I have experience with technologies like Python, Apache Airflow, SQL, AWS, Docker, and BigQuery.",
        "resume_link": "https://drive.google.com/file/d/1JdXJR5ZBGbcPkslxHYLH3ZPiYYQzJnIt/view?usp=sharing",
        "github_link": "https://github.com/MeetK208/",
        "Linkdin": "https://www.linkedin.com/in/meetkothari208/",
        "email": "meetkothari208@gmail.com"
    }
    return about_me_data

