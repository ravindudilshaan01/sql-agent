import sqlite3
from faker import Faker
import random

# Install faker first: pip install faker
fake = Faker()

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

# Fill with fake data
for i in range(1, 51):
    cursor.execute("INSERT INTO customers VALUES (?,?,?,?)",
        (i, fake.name(), fake.email(), fake.city()))

categories = ["Electronics", "Clothing", "Books", "Food"]
for i in range(1, 21):
    cursor.execute("INSERT INTO products VALUES (?,?,?,?)",
        (i, fake.word().capitalize()+" Pro", random.choice(categories), round(random.uniform(5, 500), 2)))

import datetime
for i in range(1, 101):
    date = fake.date_between(start_date="-1y", end_date="today")
    cursor.execute("INSERT INTO orders VALUES (?,?,?,?,?)",
        (i, random.randint(1,50), random.randint(1,20), random.randint(1,5), str(date)))

conn.commit()
conn.close()
print("Database created successfully!")
