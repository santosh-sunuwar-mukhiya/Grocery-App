import sqlite3
import os
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "grocery_store.db"

__cnx = None


def get_sql_connection():
    """Get or create SQLite connection"""
    global __cnx
    if __cnx is None:
        print(f"Opening sqlite connection at {DATABASE_PATH}")
        __cnx = sqlite3.connect(str(DATABASE_PATH), check_same_thread=False)
        __cnx.row_factory = sqlite3.Row
    return __cnx


def init_database():
    """Initialize databases with required tables"""
    conn = sqlite3.connect(str(DATABASE_PATH))
    cursor = conn.cursor()

    # Create uom table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS uom (
            uom_id INTEGER PRIMARY KEY AUTOINCREMENT,
            uom_name VARCHAR(45) NOT NULL
        )
    """
    )

    # Create products table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL,
            uom_id INTEGER NOT NULL,
            price_per_unit REAL NOT NULL,
            FOREIGN KEY (uom_id) REFERENCES uom(uom_id)
        )
    """
    )

    # Create orders table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name VARCHAR(100) NOT NULL,
            total REAL NOT NULL,
            datetime TIMESTAMP NOT NULL
        )
    """
    )

    # Create order_details table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_details (
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
    """
    )

    # Insert sample data if tables are empty
    cursor.execute("SELECT COUNT(*) FROM uom")
    if cursor.fetchone()[0] == 0:
        # Insert UOM data
        cursor.executemany(
            "INSERT INTO uom (uom_name) VALUES (?)",
            [("kg",), ("liter",), ("piece",), ("pack",)],
        )

    conn.commit()
    conn.close()
    print("Database initialized successfully")
