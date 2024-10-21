import random
import json
from faker import Faker
from datetime import timedelta

# Python Faker API to Create Dummy Data It has many class to generating dummy data
fake = Faker()

# Function to generate dummy data
def generate_dummy_data(num_records=100, duplicate_ratio=0.2):
    data = []
    
    for i in range(num_records):
        # Generate unique data
        record = {
            "customer_id": random.randint(1, 20),
            "transaction_amount": round(random.uniform(10.0, 1000.0), 2),
            "mob_no": fake.phone_number(),
            "transaction_datetime": fake.date_time_between(start_date='-3d', end_date='now').strftime('%Y-%m-%d %H:%M:%S'),
            "pincode": fake.postcode()
        }
        data.append(record)
    

    num_duplicates = int(num_records * duplicate_ratio)
    duplicates = random.sample(data, num_duplicates)
    data.extend(duplicates) 

    return data

dummy_data = generate_dummy_data(num_records=200, duplicate_ratio=0.3)

output_file = "dummy_transaction_data.json"
with open(output_file, "w") as f:
    json.dump(dummy_data, f, indent=4)

print(f"Data saved to {output_file}")