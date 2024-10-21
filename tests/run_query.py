import sqlite3
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.logger import setup_console_logger

# Setup logger
logger = setup_console_logger()
load_dotenv(".env")

def execute_query(query):
    # Load the database path from environment variable
    SQLALCHEMY_DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URL')
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
        db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")  # Remove SQLite URL prefix
    else:
        raise ValueError("Invalid SQLite URL format.")

    try:
        # Connect to the SQLite database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        print(query)
        # Execute the query
        print(cursor.execute(query))
        cursor.execute(query)
        # If the query is a SELECT statement, fetch the results
        if query.strip().lower().startswith("select"):
            results = cursor.fetchall()  # Fetch all results
            return results
        else:
            connection.commit()  # Commit changes for INSERT/UPDATE/DELETE

        return "Query executed successfully."
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None

    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

# Example usage
if __name__ == "__main__":
    sql_query = 'SELECT * FROM "transaction"'
    delete_query = "DELETE FROM \"transaction\" WHERE pincode = 'string';"
    result = execute_query(sql_query)
    print(result)
