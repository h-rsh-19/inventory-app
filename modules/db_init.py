# modules/db_init.py

import sqlite3
from pathlib import Path

def init_db():
    Path("db").mkdir(exist_ok=True)
    conn = sqlite3.connect('db/inventory.db')
    c = conn.cursor()

    # Users (Roles: admin, billing, inventory)
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    ''')

    # Products
    c.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        barcode TEXT UNIQUE,
        batch TEXT,
        category TEXT,
        size TEXT,
        color TEXT,
        cost_price REAL,
        retail_price REAL,
        wholesale_price REAL,
        quantity INTEGER,
        warehouse TEXT,
        section TEXT
    )
    ''')

    # Suppliers
    c.execute('''
    CREATE TABLE IF NOT EXISTS suppliers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        contact TEXT
    )
    ''')

    # Purchases
    c.execute('''
    CREATE TABLE IF NOT EXISTS purchases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        supplier_id INTEGER,
        quantity INTEGER,
        date TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id),
        FOREIGN KEY(supplier_id) REFERENCES suppliers(id)
    )
    ''')

    # Sales
    c.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        price_type TEXT,
        date TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    ''')

    # Create default users (admin / billing / inventory)
    try:
        c.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin')")
        c.execute("INSERT INTO users (username, password, role) VALUES ('billing', 'bill123', 'billing')")
        c.execute("INSERT INTO users (username, password, role) VALUES ('stockman', 'stock123', 'inventory')")
    except sqlite3.IntegrityError:
        pass  # Already inserted

    conn.commit()
    conn.close()
