from models.transactionDb import Transaction
from models.user import User
from utils.db_connect import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import func
from utils.schema import TransactionCreate
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

# Check if a duplicate transaction exists
def check_duplicate(data: dict) -> bool:
    db: Session = SessionLocal()
    try:
        cus_id = data['customer_id']
        trans_time = data['transaction_datetime']

        # Query to find duplicate records
        matching_records = db.query(Transaction).filter(
            Transaction.customer_id == cus_id,
            Transaction.transaction_datetime == trans_time
        ).all()

        if matching_records:
            logger.info(f"Duplicate Entry Found for User ID {cus_id}")
            return True  # Duplicate found
        else:
            logger.info(f"Unique Entry, Adding to DB for User ID {cus_id}")
            return False  # No duplicates found
    except Exception as e:
        logger.exception(f"Failed to check for duplicate transactions: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while checking for duplicates.")
    finally:
        db.close()

# Aggregate transaction data for a customer
def aggregate_data(cus_id: int) -> dict:
    db: Session = SessionLocal()
    try:
        # Query to find records for a specific customer
        query = db.query(Transaction).filter(
            Transaction.customer_id == cus_id
        )

        # Convert the query to a Pandas DataFrame
        df = pd.read_sql_query(query.statement, db.bind)

        # Create response with aggregated data
        response = {
            "total_transactions": len(df),
            "total_amount": df["transaction_amount"].sum(),
        }
        logger.info(f"Customer Aggregation Completed for ID {cus_id}")
        return response
    except Exception as e:
        logger.exception(f"An error occurred during aggregation: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred during data aggregation.")
    finally:
        db.close()

# Fetch paginated transaction data
async def get_all_transactions(page: int = 1, page_size: int = 10) -> dict:
    db: Session = SessionLocal()
    try:
        if page_size > 20:
            page_size = 20
        logger.info(f"Fetching transactions: page={page}, page_size={page_size}")

        total_transactions = db.query(func.count(Transaction.customer_id)).scalar()
        total_pages = (total_transactions // page_size) + (1 if total_transactions % page_size > 0 else 0)

        # Add sorting by transaction_datetime (you can change to any relevant field)
        transactions = db.query(Transaction).order_by(Transaction.id) \
            .offset((page - 1) * page_size).limit(page_size).all()

        next_page_url = f"/transaction/get-all-transactions?page={page + 1}&page_size={page_size}" if page < total_pages else None

        response = {
            'status': 'success',
            'message': "Transaction Data",
            'status_code': status.HTTP_200_OK,
            'customer_info': transactions,
            'total_responses': len(transactions),
            'total_pages': total_pages,
            'current_page': page,
            'next_page_url': next_page_url
        }
        logger.info("Transactions fetched successfully!")
        return response
    except asyncio.CancelledError:
        logger.warning("Request was canceled by the client.")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request was canceled.")
    except Exception as e:
        logger.exception(f"Failed to fetch transactions: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while fetching transactions.")
    finally:
        db.close()

# Create a new transaction
async def create_transaction(transaction: TransactionCreate) -> dict:
    db: Session = SessionLocal()
    try:
        # Check for duplicate transactions
        if check_duplicate(transaction.dict()):
            logger.info(f"Duplicate Transaction: {transaction.dict()}")
            return {
                'status': 'error',
                'message': "Data is already present in the system",
                'status_code': status.HTTP_409_CONFLICT,
                'customer_info': transaction
            }
            
        user = db.query(User).filter(User.id == transaction.customer_id).first()
        
        if not user:
            logger.warning(f"No user found with ID: {transaction.customer_id}")
            return  {
            'status': 'error',
            'message': "customer_id Not Found in System. Please Add Customer!!",
            'status_code': status.HTTP_400_BAD_REQUEST,
            "customer_id": transaction.customer_id,
            "name": "",
            "total_transactions": 0,
            "total_amount": 0
        }
            
        logger.info(f"Creating a new transaction: {transaction.dict()}")
        new_transaction = Transaction(**transaction.dict())
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        # Aggregate customer data after transaction creation
        customer_aggregated_data = aggregate_data(transaction.customer_id)

        logger.info(f"Transaction created successfully for User ID: {new_transaction.customer_id}")
        transaction_data = {
            'status': 'success',
            'message': "Transaction recorded successfully",
            'status_code': status.HTTP_201_CREATED,
            "customer_id": transaction.customer_id,
            "name": user.name,
            "total_transactions": customer_aggregated_data['total_transactions'],
            "total_amount": customer_aggregated_data["total_amount"]
        }
        return transaction_data
    except asyncio.CancelledError:
        logger.warning("Request was canceled by the client.")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request was canceled.")
    except Exception as e:
        logger.exception(f"Failed to create transaction: {e}")
        db.rollback()  # Rollback in case of error
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occurred while creating the transaction.")
    finally:
        db.close()



async def get_Customer_Ranges_transactions(min_amount: int, max_amount: int, time_period: str = None) -> dict:    
    
    logger.info(" Min_amount %s , Max_amount %s , Time range is %s", min_amount, max_amount, time_period)
    if time_period is None:
        time_period = datetime.now()
    else:
        try:
            # Parse the time_period to ensure it's in the correct format
            time_period = parser.parse(time_period)
            logger.info("DateTime Format is Valid")
        except ValueError:
            logger.exception(f"DateTime Format is not Valid {time_period}")
            return {
                'status': 'error',
                'message': "Incorrect DateTime Format",
                'status_code': status.HTTP_400_BAD_REQUEST,
            }

    db: Session = SessionLocal()
    
    try:
        filters = []
        if min_amount != None:
            filters.append(Transaction.transaction_amount >= min_amount)
        if max_amount != None:
            filters.append(Transaction.transaction_amount <= max_amount)
        if time_period:
            filters.append(Transaction.transaction_datetime <= time_period)

        query = (
            db.query(User.name, Transaction.customer_id, Transaction.transaction_amount)
            .join(Transaction, User.id == Transaction.customer_id)
            .filter(*filters)  # Apply filters using unpacking
        )


        df = pd.read_sql_query(query.statement, db.bind)
        groupbycusID = df.groupby(['customer_id', 'name'])['transaction_amount'].sum().reset_index()
        sortedDF = groupbycusID.sort_values(by='customer_id', ascending=True)
        
        return {
            'status': 'success',
            'message': "Transaction Data",
            'status_code': status.HTTP_200_OK,
            'data': sortedDF.to_dict(orient='records')
        }
    
    except asyncio.CancelledError:
        logger.warning("Request was canceled by the client.")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request was canceled.")
    except Exception as e:
        logger.exception(f"Failed to fetch customer range transactions: {e}")
        return {
            'status': 'error',
            'message': "An error occurred while fetching transactions.",
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
    finally:
        db.close()
        
async def user_transaction_by_state(state: str) -> dict:
    
    db: Session = SessionLocal()
    try:
        filter = []
        filter.append(func.lower(User.state) == state.lower())

        query = (
            db.query(User.name, User.state, Transaction.customer_id, Transaction.transaction_amount, Transaction.pincode)
            .join(Transaction, User.id == Transaction.customer_id)
            .filter(*filter)
        ).order_by(User.id)

        df = pd.read_sql_query(query.statement, db.bind)
        
        groupbycusID = df.groupby(['pincode', 'customer_id', 'name'])['transaction_amount'].sum().reset_index()
        groupbycusID = groupbycusID.sort_values(by='transaction_amount', ascending=False)

        cus_limit = 5
        result = {}

        # Iterate over each group of pincode
        for pincode, group in groupbycusID.groupby('pincode'):
            top_customers = group.head(cus_limit).reset_index()
            # print(top_customers)
            customer_list = []
            for key, row in top_customers.iterrows():
                # print("--------------------------------------------",key)
                customer_info = {
                    'customer_id': row['customer_id'],
                    'name': row['name'],
                    'total_transaction_amount': row['transaction_amount']
                }
                customer_list.append(customer_info)
            
            result[f'pincode_{pincode}'] = customer_list


        return {
            'status': 'succcess',
            'message': "Data Found",
            'status_code': status.HTTP_200_OK,
            f"{state}_state_data": result
            }
    
    except asyncio.CancelledError:
        # logger.warning("Request was canceled by the client.")
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="Request was canceled.")
    except Exception as e:
        logger.exception(f"Failed to fetch customer range transactions: {e}")
        return {
            'status': 'error',
            'message': "An error occurred while fetching transactions.",
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        }
    return {
            'status': 'error',
            'message': "An error occurred while fetching Information.",
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        }