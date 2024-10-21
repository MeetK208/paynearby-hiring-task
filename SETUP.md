# DE Assignment - Meet Kothari

This project is a Data Engineering assignment for PayNearby. The application is built using FastAPI to handle transactions and provides a simple API interface.

## Tech Stack

Backend: FastAPI (Python) \
Database: PostgreSQL \
API: REST API \
Environment: Docker for containerization, SQLAlchemy for ORM \

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/analytics1211/de-aso-assigment-meetkothari208.git
```

### 2. Create a Virtual Environment

```bash
python -m venv paynearbyEnv
```

### 3. Activate the Virtual Environment

- For Windows:

  ```bash
  .\paynearbyEnv\Scripts\Activate
  ```

- For macOS/Linux:

  ```bash
  source paynearbyEnv/bin/activate
  ```

### 4. Install Project Dependencies

```bash
pip install -r requirements.txt
```

### 5. Navigate to the Main Application Folder

```bash
cd transaction-app
```

### 6. Set Up Environment Variables

Create a `.env` file in the `transaction-app` directory and add the following variable:

```bash
SQLALCHEMY_DATABASE_URL=<YOUR_DATABASE_URL>
```

Make sure to replace `<YOUR_DATABASE_URL>` with your actual database URL.

### 7. Run the Application

```bash
uvicorn main:app --reload
```

### 8. Test All Endpoints

Open a browser (preferably Chrome) and navigate to:

```bash
http://localhost:<your_PORT>/docs
```

Here you can view and interact with all API endpoints via the automatically generated Swagger UI.

### Additional Notes

- Ensure that Python 3.8+ is installed.
- If you encounter any database connection issues, verify that the SQLALCHEMY_DATABASE_URL is correctly set in your .env file.
- For testing, you can use tools like Postman or the built-in Swagger UI.
- Make sure to use "My-DB" to test the project; I have already added dummy data in it.
- If you want to add a new Transaction, first check whether the customer is already in the database. If not, add the customer first before proceeding with the transaction.
