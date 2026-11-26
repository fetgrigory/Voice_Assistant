import logging
import datetime

from src.db.database import session_factory
from src.db.models import Event


logger = logging.getLogger(__name__)


# Inserts a new event into the database
def add_event(
    description: str,
    event_date: str,
    event_time: str,
    reminder_minutes: int = 60,
) -> bool:
    with session_factory() as session:
        try:
            event_at = datetime.datetime.strptime(
                f"{event_date} {event_time}", "%Y-%m-%d %H:%M:%S"
            )

            event = Event(
                description=description,
                event_at=event_at,
                remind_before_minutes=reminder_minutes,
                is_sent=False,
            )

            session.add(event)
            session.commit()

            return True
        except Exception as e:
            session.rollback()
            logger.error("Ошибка при добавлении события: %s", e)

            return False


# Returns all events from the database, ordered by time
def get_all_events() -> list[dict] | None:
    try:
        with session_factory() as session:
            events = session.query(Event).order_by(Event.event_at).all()

            return [
                {
                    "id": event.id,
                    "description": event.description,
                    "event_at": event.event_at,
                    "remind_before_minutes": event.remind_before_minutes,
                    "is_sent": event.is_sent,
                }
                for event in events
            ]

    except Exception as e:
        logger.error("Ошибка при получении событий: %s", e)
        return None
