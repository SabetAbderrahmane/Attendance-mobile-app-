from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Attendance(Base):
    __tablename__ = "attendance_records"
    __table_args__ = (
        UniqueConstraint("user_id", "event_id", name="uq_attendance_user_event"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)
    checked_in_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
