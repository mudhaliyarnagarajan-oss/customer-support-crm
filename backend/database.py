from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///crm.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE,
            customer_name TEXT,
            customer_email TEXT,
            subject TEXT,
            description TEXT,
            status TEXT
        )
    """))
    conn.commit()

from sqlalchemy import text
from database import engine

with engine.connect() as conn:
    # conn.execute(
    #     text("""
    #     ALTER TABLE tickets
    #     ADD COLUMN priority TEXT DEFAULT 'Medium'
    #     """)
    # )
    conn.commit()
    from sqlalchemy import text
from database import engine

with engine.connect() as conn:
    result = conn.execute(text("PRAGMA table_info(tickets)"))

    for row in result:
        print(row)

print("Priority column added")

print("Database Ready")