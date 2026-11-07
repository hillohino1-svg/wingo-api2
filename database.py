import sqlite3

def get_db():
    conn = sqlite3.connect("wingo.db")
    conn.row_factory = sqlite3.Row

    conn.execute("""
    CREATE TABLE IF NOT EXISTS history(
        issue TEXT PRIMARY KEY,
        number INTEGER,
        color TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    return conn
