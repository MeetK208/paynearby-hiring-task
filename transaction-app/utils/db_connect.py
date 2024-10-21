from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from .logger import setup_console_logger

# Setup logger
logger = setup_console_logger()
load_dotenv(".env")

# Define the base class for declarative models

try:
    SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
    if SQLALCHEMY_DATABASE_URL is None:
        raise ValueError("SQLALCHEMY_DATABASE_URL environment variable not set.")

    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("DB Connection established successfully and tables created if they did not exist.")
except Exception as e:
    logger.exception("DB Connection Failed with Exception:")
