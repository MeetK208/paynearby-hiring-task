# Transaction API Documentation

## Overview

This API provides endpoints to manage and retrieve transaction and user data. It supports operations such as creating new transactions, fetching transactions with pagination, aggregating transaction data, and retrieving user data based on filters.

**functionalities/features** of transaction API:

### Transaction Management

1. **Create New Transaction**:

   - Users can create new transactions by providing necessary details like `customer_id`, `transaction_amount`, `mobile number`, and `transaction_datetime`.
   - Duplicate transactions are prevented by checking if a transaction with the same `customer_id` and `transaction_datetime` already exists.

2. **Get All Transactions**:

   - Users can view all recorded transactions with pagination support.
   - Allows setting the number of transactions per page and fetching subsequent pages using query parameters.

3. **Filter Transactions by Range**:

   - Users can filter transactions based on a transaction amount range (`min_amount` and `max_amount`).
   - An optional time period filter can also be used to fetch transactions within a specific date range.

4. **View Transactions by User's State**:
   - Users can retrieve top transactions grouped by the customer's state and pincode.
   - Limits the response to the top 5 customers per pincode within the state.

### User Management

1. **Create New User**:

   - Users can register new accounts by providing details like their name and state.

2. **View All Users**:

   - Users can view all registered users with pagination and optional filtering by state.
   - Provides information like total users, number of users on the current page, and next page URL.

3. **Search User by Customer ID**:
   - Users can search for specific users by their customer ID and retrieve their details.

### Additional Functionalities

1. **Error Handling and Response**:
   - The API provides detailed error handling for duplicate transactions, incorrect input formats, and server errors.
2. **Pagination**:
   - Pagination support is provided for fetching both transactions and user data, allowing users to control the number of records per page.

## API Endpoints

### 1. **Create a New Transaction** (`POST /transaction/create-transaction`)

Creates a new transaction entry after checking for duplicates.

- **Request Body**:
  ```json
  {
    "customer_id": 0,
    "transaction_amount": 0,
    "mob_no": "string",
    "transaction_datetime": "2024-09-30T16:23:55.494Z",
    "pincode": "string"
  }
  ```
- **Response** (Success - 201 Created):
  ```json
  {
    "status": "success",
    "message": "Transaction recorded successfully",
    "status_code": 201,
    "customer_id": 123,
    "name": "John Doe",
    "total_transactions": 5,
    "total_amount": 1250.5
  }
  ```
- **Error Responses**:
  - 409 Conflict: Duplicate transaction detected.
  - 500 Internal Server Error: An error occurred while creating the transaction.

### 2. **Get All Transactions** (`GET /transactions/get-all-transactions`)

Fetches paginated transaction data.

- **Query Parameters**:

  - `page` (integer, optional): Page number (default: 1).
  - `page_size` (integer, optional): Number of transactions per page (max: 20).

- **Response** (Success - 200 OK):
  ```json
  {
    "status": "success",
    "message": "Transaction Data",
    "status_code": 200,
    "customer_info": [...],
    "total_responses": 10,
    "total_pages": 5,
    "current_page": 1,
    "next_page_url": "/transaction/get-all-transactions?page=2&page_size=10"
  }
  ```
- **Error Responses**:
  - 500 Internal Server Error: An error occurred while fetching transactions.

### 3. **Get Transactions by Range** (`GET /transactions/min-max-filter`)

Fetches customer transactions filtered by amount range and an optional time period.

- **Query Parameters**:

  - `min_amount` (integer, optional): Minimum transaction amount.
  - `max_amount` (integer, optional): Maximum transaction amount.
  - `time_period` (string, optional): Date and time filter (ISO format).

- **Response** (Success - 200 OK):
  ```json
  [
    {
      "customer_id": 123,
      "name": "John Doe",
      "transaction_amount": 1000.5
    },
    {
      "customer_id": 456,
      "name": "Jane Doe",
      "transaction_amount": 750.25
    }
  ]
  ```
- **Error Responses**:
  - 400 Bad Request: Incorrect DateTime format.
  - 500 Internal Server Error: An error occurred while fetching transactions.

### 4. **Get User Transactions by State** (`GET /transactions/user-by-states?state=gujarat`)

Fetches the top transactions grouped by user state and pincode, limited to 5 customers per pincode.

- **Path Parameters**:

  - `state` (string, required): The state to filter transactions by.

- **Response** (Success - 200 OK):
  ```json
  {
    "status": "success",
    "message": "Data Found",
    "status_code": 200,
    "gujarat_state_data": {
      "pincode_123456": [
        {
          "customer_id": 123,
          "name": "John Doe",
          "total_transaction_amount": 2500.75
        },
        {
          "customer_id": 456,
          "name": "Jane Doe",
          "total_transaction_amount": 2000.25
        }
      ]
    }
  }
  ```
- **Error Responses**:
  - 500 Internal Server Error: An error occurred while fetching transactions.

### 5. **Create a New User** (`POST /register/create-user`)

Creates a new user in the system.

- **Request Body**:

  ```json
  {
    "name": "John Doe",
    "state": "New York"
  }
  ```

- **Response** (Success - 201 Created):

  ```json
  {
    "status": "success",
    "message": "User created successfully",
    "status_code": 201,
    "user_info": {
      "id": 1,
      "name": "John Doe",
      "state": "New York"
    }
  }
  ```

- **Error Responses**:
  - 500 Internal Server Error: An error occurred while creating the user.

### 6. **Get All Users** (`GET /register/get-all-user`)

Fetches paginated user data, with an optional filter by state.

- **Query Parameters**:

  - `state` (string, optional): Filter users by state.
  - `page` (integer, optional): Page number (default: 1).
  - `page_size` (integer, optional): Number of users per page (max: 20).

- **Response** (Success - 200 OK):

  ```json
  {
    "status": "success",
    "message": "User Data",
    "status_code": 200,
    "user_info": [...],
    "total_users": 50,
    "current_page_users": 10,
    "total_pages": 5,
    "current_page": 1,
    "next_page_url": "/register/get-all-user?page=2&page_size=10&state=New York"
  }
  ```

- **Error Responses**:
  - 500 Internal Server Error: An error occurred while fetching user data.

### 7. **Search User by Customer ID** (`GET /register/search-user-id?cus_id=1`)

Searches for a user by their customer ID.

- **Path Parameters**:

  - `cus_id` (integer): The customer ID to search for.

- **Response** (Success - 200 OK):

  ```json
  {
    "status": "success",
    "message": "Customer ID Found in System",
    "status_code": 200,
    "user_info": {
      "id": 123,
      "name": "John Doe",
      "state": "New York"
    }
  }
  ```

- **Error Responses**:
  - 404 Not Found: No user found with the provided customer ID.
  - 500 Internal Server Error: An error occurred while fetching user data.

## Assumptions

- **Duplicate Check**: Transactions are considered duplicates if the `customer_id` and `transaction_datetime` match.
- **Pagination**: Limits the number of records returned per page to 20.
- **Database**: SQLite is used with SQLAlchemy as the ORM.
- **Logging**: A custom logger is used to log information and errors.
- **Date Formats**: The time period should be provided in ISO 8601 format for date-based filters.

## Error Handling

- Each API implements detailed error handling with appropriate status codes.
  - **409 Conflict**: For duplicate transaction entries.
  - **400 Bad Request**: For incorrect input formats.
  - **500 Internal Server Error**: For unforeseen issues during API execution.
