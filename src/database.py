import logging
import sqlite3
def get_db():
    conn = sqlite3.connect("items.db")
    conn.row_factory = sqlite3.Row
    return conn
def startup_event():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price REAL, is_offer INTEGER)")
    conn.commit()
    logging.debug("Database created!")
