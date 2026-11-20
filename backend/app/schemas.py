from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TicketIn(BaseModel):
    message: str = Field(min_length=3, max_length=5000)


class TicketUpdate(BaseModel):
    status: str | None = None
    suggested_reply: str | None = None


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    message: str
    category: str
    category_conf: float
    urgency: str
    urgency_conf: float
    retrieval_score: float
    suggested_reply: str | None
    status: str
    created_at: datetime | None


class StatsOut(BaseModel):
    total: int
    auto_replied: int
    escalated: int
    sent: int
