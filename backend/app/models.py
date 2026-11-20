from datetime import datetime

from sqlalchemy import String, Text, Float, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50))
    category_conf: Mapped[float] = mapped_column(Float)
    urgency: Mapped[str] = mapped_column(String(20))
    urgency_conf: Mapped[float] = mapped_column(Float)
    retrieval_score: Mapped[float] = mapped_column(Float)
    suggested_reply: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20))  # auto_replied | escalated | sent
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
