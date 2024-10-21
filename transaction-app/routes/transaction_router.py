from fastapi import APIRouter, Query
from services import transaction as transaction_service
from datetime import datetime
import math
from typing import Optional

router = APIRouter()
MOST_NEGATIVE_FLOAT = -3.4028235e+38
MOST_POSITIVE_FLOAT = 3.4028235e+38

@router.get("/get-all-transactions")
async def get_all_transactions(
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    page_size: int = Query(10, ge=1, description="Number of transactions per page, default is set to 10")
):
    return await transaction_service.get_all_transactions(page, page_size)

@router.post("/create-transaction")
async def create_transaction(transaction: transaction_service.TransactionCreate):
    return await transaction_service.create_transaction(transaction)

@router.get("/min-max-filter")
async def create_transaction(
    min_amount: Optional[float] = Query(None, description="Minimum transaction amount."),
    max_amount: Optional[float] = Query(None, description="Maximum transaction amount."),
    time_period: str = Query(str(datetime.now()), description="Please provide the transaction date limit.")
):
    return await transaction_service.get_Customer_Ranges_transactions(min_amount, max_amount, time_period)


@router.get("/user-by-states")
async def user_transaction_by_state(state: str):
    return await transaction_service.user_transaction_by_state(state)
