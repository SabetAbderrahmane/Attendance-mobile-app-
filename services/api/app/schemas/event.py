from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str | None = None
    location: str | None = Field(default=None, max_length=255)
    starts_at: datetime
    ends_at: datetime


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
