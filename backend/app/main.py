from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import CORS_ORIGINS
from app.db import engine, get_db
from app.models import Base, Ticket
from app.schemas import TicketIn, TicketUpdate, TicketOut, StatsOut
from app.services.pipeline import process_ticket


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)  # tables startup par bante hain
    yield


app = FastAPI(title="SmartTriage", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api/tickets", response_model=TicketOut)
def create_ticket(body: TicketIn, db: Session = Depends(get_db)):
    result = process_ticket(body.message)
    ticket = Ticket(message=body.message, **result)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@app.get("/api/tickets", response_model=list[TicketOut])
def list_tickets(db: Session = Depends(get_db)):
    return db.scalars(select(Ticket).order_by(Ticket.created_at.desc())).all()


@app.get("/api/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket nahi mila")
    return ticket


@app.patch("/api/tickets/{ticket_id}", response_model=TicketOut)
def update_ticket(ticket_id: int, body: TicketUpdate, db: Session = Depends(get_db)):
    ticket = db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket nahi mila")
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(ticket, field, value)
    db.commit()
    db.refresh(ticket)
    return ticket


@app.get("/api/stats", response_model=StatsOut)
def stats(db: Session = Depends(get_db)):
    total = db.scalar(select(func.count(Ticket.id))) or 0

    def count(status: str) -> int:
        return db.scalar(select(func.count(Ticket.id)).where(Ticket.status == status)) or 0

    return StatsOut(
        total=total,
        auto_replied=count("auto_replied"),
        escalated=count("escalated"),
        sent=count("sent"),
    )
