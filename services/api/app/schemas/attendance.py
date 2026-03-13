from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttendanceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    event_id: int
    checked_in_at: datetime
