from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "CRM API Running"}


@app.post("/tickets")
def create_ticket(
    customer_name: str,
    customer_email: str,
    subject: str,
    description: str
):
    with engine.connect() as conn:

        last_id = conn.execute(
            text("SELECT MAX(id) FROM tickets")
        ).scalar()

        if last_id is None:
            last_id = 0

        ticket_id = f"TKT-{last_id + 1:03d}"

        conn.execute(
            text("""
                INSERT INTO tickets
                (ticket_id, customer_name, customer_email, subject, description, status)
                VALUES
                (:ticket_id, :customer_name, :customer_email, :subject, :description, :status)
            """),
            {
                "ticket_id": ticket_id,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "subject": subject,
                "description": description,
                "status": "Open"
            }
        )

        conn.commit()

    return {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "subject": subject,
        "description": description,
        "status": "Open"
    }


@app.get("/tickets")
def get_tickets(
    status: str = Query(None),
    search: str = Query(None)
):
    with engine.connect() as conn:

        rows = conn.execute(
            text("""
                SELECT ticket_id,
                       customer_name,
                       customer_email,
                       subject,
                       description,
                       status
                FROM tickets
            """)
        )

        result = []

        for row in rows:
            result.append({
                "ticket_id": row.ticket_id,
                "customer_name": row.customer_name,
                "customer_email": row.customer_email,
                "subject": row.subject,
                "description": row.description,
                "status": row.status
            })

    if status:
        result = [
            ticket for ticket in result
            if ticket["status"].lower() == status.lower()
        ]

    if search:
        search = search.lower()

        result = [
            ticket for ticket in result
            if (
                search in ticket["customer_name"].lower()
                or search in ticket["customer_email"].lower()
                or search in ticket["subject"].lower()
                or search in ticket["description"].lower()
            )
        ]

    return result


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: str):
    with engine.connect() as conn:

        row = conn.execute(
            text("""
                SELECT ticket_id,
                       customer_name,
                       customer_email,
                       subject,
                       description,
                       status
                FROM tickets
                WHERE ticket_id = :ticket_id
            """),
            {"ticket_id": ticket_id}
        ).fetchone()

    if row:
        return {
            "ticket_id": row.ticket_id,
            "customer_name": row.customer_name,
            "customer_email": row.customer_email,
            "subject": row.subject,
            "description": row.description,
            "status": row.status
        }

    return {"error": "Ticket not found"}


@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, status: str):

    with engine.connect() as conn:

        conn.execute(
            text("""
                UPDATE tickets
                SET status = :status
                WHERE ticket_id = :ticket_id
            """),
            {
                "ticket_id": ticket_id,
                "status": status
            }
        )

        conn.commit()

    return {
        "message": "Ticket updated",
        "ticket_id": ticket_id,
        "status": status
    }

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: str):

    with engine.connect() as conn:

        conn.execute(
            text("""
                DELETE FROM tickets
                WHERE ticket_id = :ticket_id
            """),
            {"ticket_id": ticket_id}
        )

        conn.commit()

    return {
        "message": "Ticket deleted successfully",
        "ticket_id": ticket_id
    }