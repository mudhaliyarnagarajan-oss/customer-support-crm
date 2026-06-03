from fastapi import FastAPI, Query

app = FastAPI()

tickets = []


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
    ticket_id = f"TKT-{len(tickets) + 1:03d}"

    ticket = {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "subject": subject,
        "description": description,
        "status": "Open"
    }

    tickets.append(ticket)

    return ticket


@app.get("/tickets")
def get_tickets(
    status: str = Query(None),
    search: str = Query(None)
):
    result = tickets

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
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            return ticket

    return {"error": "Ticket not found"}


@app.put("/tickets/{ticket_id}")
def update_ticket(ticket_id: str, status: str):
    for ticket in tickets:
        if ticket["ticket_id"] == ticket_id:
            ticket["status"] = status
            return ticket

    return {"error": "Ticket not found"}