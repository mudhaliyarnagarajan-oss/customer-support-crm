from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///crm.db"

engine = create_engine(DATABASE_URL)

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

print("Tickets table created successfully!")