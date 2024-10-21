<<<<<<< HEAD
# Paynearby Data Engineering Assignment

# Overview

Thank you for your interest in joining PayNearby!   
As part of our selection process, all of our candidates must complete an assignment.  
The test is designed to assess key competencies required in your role as a data engineer at PayNearby.

* Please **submit** your answers in a **different branch** and **create a pull request**.   
* Please do not merge your own pull request.

**Note**: *While we love open source here at PayNearby, please do not create a public repo with your test in!*   
*This challenge is only shared with people interviewing, and for obvious reasons we'd like it to remain this way.*

At PayNearby, We make financial services simple and accessible for everyone.   
Since 2016, our mission has been to bring services to your neighborhood through local retailers and small businesses  
A few such services are mentioned below.

* Banking  
* Digital payments  
* Insurance  
* Investment services

With over 1.5 million retail partners across 17,000+ PIN codes in India, we're proud to have processed more than 2 billion transactions.   
As part of the data engineering team, we ensure everything runs smoothly by managing and analyzing this vast amount of data to continuously improve our services.

# Exercise
The goal of this exercise is to write a service that can ingest transaction data from a personal banking app into a relational database and provide APIs to query the customer data based on various criteria.

**1. Develop an API to ingest data into the database.**

  * Ingest value into the database:

      * Objective: Design an API that accepts transaction data and inserts it into the database, handling any duplicate records.
      
      * Parameters: The API must accept the following arguments:
          ```
          {
            customer_id : int,
            transaction_amount : float,
            mob_no : string,
            transaction_datetime : datetime,
            pincode : string
          }
          ```
      
      * Sample request:
        ```
            {
              "customer_id": 101,
              "transaction_amount": 1500.75,
              "mob_no": "9876543210",
              "transaction_datetime": "2024-09-24T15:30:00",
              "pincode": "110001"
            }
          ```
      
      * Response: Return customer info for those who have made transactions. If a duplicate record is detected (same customer, same transaction timestamp), handle appropriately (e.g., log or return a message).
      
      * Sample Response:
        ```
            {
              "message": "Transaction recorded successfully",
              "customer_info": {
                "customer_id": 101,
                "name": "John Doe",
                "total_transactions": 15,
                "total_amount": 25000.50
              }
            }
        ```

Note: Handle duplicate records while inserting the data. 


**2. Develop an API to Query Customer Transactions Between Amount Ranges.**
  
  * Objective: Design an API that accepts two numbers and returns customer information for those whose total transaction amount falls between the given range.
  
  * Parameters:
          min_amount: The minimum transaction amount.
          max_amount: The maximum transaction amount.
          time_period: Date limit for total transaction amount.
  
  * Sample Request:
    
            {
              "min_amount": 50000,
              "max_amount": 200000,
              "time_period": "01/01/2038"
            }

   * Response: Return customer information, including customer ID, name, and total transaction amount till the specified time_period.

           [
             {
               "customer_id": 102,
               "name": "Jane Smith",
               "total_transaction_amount": 180000
             },
             {
               "customer_id": 104,
               "name": "Robert Johnson",
               "total_transaction_amount": 120000
             }
           ]

**3. Develop an API to Return Top 5 Transacting Customers per Pincode in a Given State.**
  
  * Objective: Design an API that returns the top 5 transacting customers for each pincode in the specified state.
  
  * Parameters:
      -state: The state for which the top customers are requested.
  
  * Sample Request:
      ```
        {
          "state": "Punjab"
        }
      ```
  
  * Response: Return the top 5 customers for each pincode in the state, sorted by total transaction amount.
  
  * Sample Response:
    ```
        {
          "pincode_141001": [
            {
              "customer_id": 201,
              "name": "Atharva Sharma",
              "total_transaction_amount": 75000
            },
            {
              "customer_id": 202,
              "name": "Simran Patel",
              "total_transaction_amount": 60000
            }
          ],
          "pincode_160001": [
            {
              "customer_id": 301,
              "name": "Lakshman Mehta",
              "total_transaction_amount": 90000
            },
            {
              "customer_id": 302,
              "name": "Ram Sharma",
              "total_transaction_amount": 85000
            }
          ]
        }
    ```

**Assumptions:**

* You are allowed to use any programming language or framework.

* You are allowed to use any database. 

### Deliverables:

**1. API Implementation:**
   - Develop all the APIs using FastAPI.

**2. Detailed Explanation:**
   - Provide a clear explanation of your approach, including the logic, assumptions, and how the solution meets the objectives. Add comments in the code where necessary.

**3. Sample Inputs:**
   - Submit sample inputs used for testing the APIs, covering typical and edge cases.

**4. Unit Tests:**
   - Write unit tests for each API, and include instructions for running them.

# Submission criteria

###
* Provide a documentation of how to setup assignment locally and test it
* Provide all the assumptions you have made in an assumptions.md file

### Pull Request

* Submit your code into a separate branch and create a pull request to the main branch.

### Code

* Follow language-specific coding conventions (PEP 8 for Python)  
* Handle Error cases with Error Handling
* Add validation and Test Cases
* Add comments wherever you feel necessary.

### Documentation

* setup.md **:** document with instructions to set up the project
* architecture.md **:** Architecture Diagram and Ingestion Process

### Good-to-Have

#### Performance Considerations

* Include any performance optimizations or considerations in the documentation. Share metrics or benchmarks if available.

#### Security

* Address any security considerations related to data handling and access control.

#### Sample Data

* Include sample data files or scenarios for testing.

#### Testing strategy

* Include a set of test cases and the tool used to run these test cases  
* Way to set up and run these test cases.



***Best Practices that should be followed while building a FastAPI app:***


1. Set up a virtual environment to isolate your project's dependencies from other Python projects on your system.

2. Break your application into modules (e.g., routers, models, services, schemas) for increased maintainability.

3. Implement a centralised logging system to capture and monitor exceptions and errors in application.
  
4. Implement versioning in your API's to ensure backward compatibility as your application evolves.

5. Avoid hardcoding and parameters instead use a config.json file for input parameters.

6. Write unit tests for your API logic and integration tests for your endpoints


You can follow App Structure as below example for best Pratices: 

```
├── app  # Contains the main application files.
│   ├── __init__.py   # this file makes "app" a "Python package"
│   ├── main.py       # Initializes the FastAPI application.
│   ├── routers
│   │   ├── __init__.py
│   │   ├── items.py  # Defines routes and endpoints related to items.
│   │   └── users.py  # Defines routes and endpoints related to users.
│   ├── services
│   │   ├── __init__.py
│   │   ├── item.py  # Defines CRUD operations logic for items.
│   │   └── user.py  # Defines CRUD operations logic for users.
│   ├── models
│   │   ├── __init__.py
│   │   ├── item.py  # Defines database models for items.
│   │   └── user.py  # Defines database models for users.
│   └── utils(helper functions)
│       ├── __init__.py
│       ├── email.py          # Defines functions for sending emails.
│       └── notification.py   # Defines functions for sending notifications
├── tests
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_items.py  # Tests for the items module.
│   └── test_users.py  # Tests for the users module.
├── requirements.txt
├── .gitignore
└── README.md
```


 
=======
# paynearby-hiring-task
>>>>>>> 8a1e2db547ed6961cc51db1ee230a969ec411eb1
