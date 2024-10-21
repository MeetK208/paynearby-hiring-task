from fastapi import APIRouter, Query
from services import transaction as transaction_controller, user_register
from datetime import datetime
import math
from typing import Optional

router = APIRouter()

@router.get("/get-all-user")
async def get_all_users(
    state: str = Query(None,  description="Please provide State to Search State vise"),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    page_size: int = Query(10, ge=1, description="Number of transactions per page, default is set to 10")
):
    return await user_register.get_all_users(state, page, page_size)

@router.post("/create-user")
async def create_user(User: user_register.UserCreate):
    return await user_register.create_user(User)

@router.get("/search-user-id")
async def search_user(
    cus_id: str = Query(...,  description="Please provide Cus ID to Search in Syatem")
):
    return await user_register.search_user(cus_id)