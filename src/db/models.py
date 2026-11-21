from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.db.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    event_at = Column(DateTime, nullable=False, index=True)
    remind_before_minutes = Column(Integer, default=30, nullable=False)
    is_sent = Column(Boolean, default=False, nullable=False)
