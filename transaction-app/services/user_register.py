from models.user import User
from utils.db_connect import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from utils.schemaUser import UserCreate
from utils.logger import setup_console_logger
from fastapi import HTTPException, status
import asyncio
import pandas as pd
from datetime import datetime
from dateutil.parser import parse
from datetime import datetime
from dateutil import parser

# Setup logger
logger = setup_console_logger()

# Fetch paginated transaction data
async def get_all_users(state: str = None, page: int = 1, page_size: int = 10) -> dict:
    db: Session = SessionLocal()
    try:
        if page_size > 20:
            page_size = 20

        searchFilter = []
        if state:
            # Convert state to lowercase using ilike for case-insensitive filtering
            searchFilter.append(func.lower(User.state) == state.lower())
            logger.info(f"Fetching User Data: page={page}, page_size={page_size} and For State {state}")

        query = db.query(User).filter(*searchFilter).order_by(User.id)
        total_users = query.count()
        
        # Recalculate total_pages correctly based on available users and page_size
        total_pages = max(1, (total_users + page_size - 1) // page_size)

        # Ensure the correct offset is applied for the current page
        offset_value = (page - 1) * page_size

        # Fetch users based on pagination
        users = query.offset(offset_value).limit(page_size).all()

        # Only generate next_page_url if there's actually a next page
        has_next_page = page < total_pages and len(users) == page_size
        next_page_url = (
            f"/register/get-all-user?page={page + 1}&page_size={page_size}&state={state}"
            if has_next_page
            else None
        )

        response = {
            'status': 'success',
            'message': "User Data",
            'status_code': status.HTTP_200_OK,
            'user_info': users,
            'total_users': total_users,
            'current_page_users': len(users),
            'total_pages': total_pages,
            'current_page': page,
            'next_page_url': next_page_url
        }
        logger.info("User Data fetched successfully!")
        return response
    except asyncio.CancelledError:
        logger.warning("Request was canceled by the client.")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request was canceled.")
    except Exception as e:
        logger.exception(f"Failed to fetch User Data: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching transactions.")
    finally:
        db.close()

# Create a new transaction
async def create_user(user: UserCreate) -> dict:
    db: Session = SessionLocal()
    try:
        # Check for duplicate users
        logger.info(f"Creating a new user: {user.dict()}")
        new_user = User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Log user creation
        logger.info(f"User created successfully with ID: {new_user.id}")

        # Return success response with the created user's data
        response_data = {
            'status': 'success',
            'message': "User created successfully",
            'status_code': status.HTTP_201_CREATED,
            'user_info': new_user,  # Return the actual new user data
        }
        return response_data
    except asyncio.CancelledError:
        logger.warning("Request was canceled by the client.")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request was canceled.")
    except Exception as e:
        logger.exception(f"Failed to create user: {e}")
        db.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the user.")
    finally:
        db.close()  # Close DB connection
        
async def search_user(cus_id: int) -> dict:
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == int(cus_id)).first()
        
        if not user:
            logger.warning(f"No user found with ID: {cus_id}")
            return {
                 'status': 'error',
                'message': "Customer Id not Found in System",
                'status_code': status.HTTP_404_NOT_FOUND,
                'user_info': {},
            }
        return {
             'status': 'success',
                'message': "Customer Id Found in System",
                'status_code': status.HTTP_200_OK,
                'user_info': user,
        }
    except asyncio.CancelledError:
        logger.warning("Request was canceled by the client.")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request was canceled.")
    except Exception as e: 
        logger.exception(f"Failed to fetch User Data: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching transactions.")
    finally:
        db.close()
