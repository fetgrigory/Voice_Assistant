import datetime

from src.db.database import session_factory
from src.db.models import Event


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
            print(f"Ошибка при добавлении события: {e}")

            return False