import csv
import random
from datetime import datetime, timedelta
from faker import Faker

def generate_large_customer_csv(filename: str, num_records: int = 5000):
    """Generate a large CSV file with customer data"""
    fake = Faker()
    
    # Define data for random selection
    occupations = [
        'Software Engineer', 'Data Scientist', 'Product Manager', 'Marketing Manager',
        'Sales Director', 'UX Designer', 'DevOps Engineer', 'Business Analyst',
        'Full Stack Developer', 'Backend Developer', 'Frontend Developer',
        'Database Administrator', 'Project Manager', 'Technical Lead',
        'Cloud Architect', 'Mobile Developer', 'QA Engineer', 'Product Owner'
    ]
    
    states = [
        'NY', 'CA', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI',
        'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI'
    ]
    
    print(f"🔄 Generating {num_records:,} customer records...")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'id', 'first_name', 'last_name', 'email', 'phone', 'address',
            'city', 'state', 'zip_code', 'country', 'registration_date',
            'age', 'gender', 'occupation', 'salary'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, num_records + 1):
            # Generate random data
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}"
            
            # Random registration date in last 2 years
            start_date = datetime.now() - timedelta(days=730)
            random_date = start_date + timedelta(days=random.randint(0, 730))
            
            record = {
                'id': i,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': fake.phone_number(),
                'address': fake.street_address(),
                'city': fake.city(),
                'state': random.choice(states),
                'zip_code': fake.zipcode(),
                'country': 'USA',
                'registration_date': random_date.strftime('%Y-%m-%d'),
                'age': random.randint(22, 65),
                'gender': random.choice(['M', 'F']),
                'occupation': random.choice(occupations),
                'salary': random.randint(45000, 150000)
            }
            
            writer.writerow(record)
            
            # Progress indicator
            if i % 1000 == 0:
                print(f"  Generated {i:,} records...")
    
    print(f"✅ Successfully generated {filename} with {num_records:,} records")

def generate_sales_csv(filename: str, num_records: int = 10000):
    """Generate sales transaction data"""
    fake = Faker()
    
    products = [
        'Laptop', 'Desktop Computer', 'Monitor', 'Keyboard', 'Mouse',
        'Tablet', 'Smartphone', 'Headphones', 'Webcam', 'Printer',
        'Router', 'Hard Drive', 'SSD', 'RAM', 'Graphics Card',
        'Motherboard', 'CPU', 'Power Supply', 'Case', 'Cooling Fan'
    ]
    
    categories = ['Electronics', 'Computers', 'Accessories', 'Components']
    
    print(f"🔄 Generating {num_records:,} sales records...")
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'transaction_id', 'customer_id', 'product_name', 'category',
            'quantity', 'unit_price', 'total_amount', 'discount',
            'transaction_date', 'payment_method', 'sales_rep'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(1, num_records + 1):
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(29.99, 2999.99), 2)
            discount = round(random.uniform(0, 0.2), 2)
            total_amount = round(quantity * unit_price * (1 - discount), 2)
            
            # Random transaction date in last year
            start_date = datetime.now() - timedelta(days=365)
            random_date = start_date + timedelta(days=random.randint(0, 365))
            
            record = {
                'transaction_id': f"TXN{i:06d}",
                'customer_id': random.randint(1, 5000),  # Reference to customers
                'product_name': random.choice(products),
                'category': random.choice(categories),
                'quantity': quantity,
                'unit_price': unit_price,
                'total_amount': total_amount,
                'discount': discount,
                'transaction_date': random_date.strftime('%Y-%m-%d %H:%M:%S'),
                'payment_method': random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash']),
                'sales_rep': fake.name()
            }
            
            writer.writerow(record)
            
            if i % 2000 == 0:
                print(f"  Generated {i:,} records...")
    
    print(f"✅ Successfully generated {filename} with {num_records:,} records")

# This file is for generating sample data if needed
# Since you have your own CSV file, you can ignore this file
# Use csv_importer.py to import your existing CSV file