import logging
from datetime import datetime
from src.db.crud import add_event, get_all_events

logger = logging.getLogger(__name__)

MSG_EMPTY_TEXT = "Текст напоминания пуст."
MSG_CREATED = 'Напоминание "{description}" создано {created_at}.'
MSG_CREATE_FAILED = "Не удалось создать напоминание. Попробуйте ещё раз."
MSG_LIST_HEADER = "Вот твои напоминания:"
MSG_LIST_EMPTY = "У тебя пока нет напоминаний."
MSG_LIST_FAILED = "Не удалось получить список напоминаний. Попробуйте ещё раз."


class ReminderManager:
    # Creates a new note and saves it to the database
    def create_reminder(self, description: str) -> dict:
        description = (description or "").strip()
        if not description:
            return {"success": False, "message": MSG_EMPTY_TEXT}

        try:
            now = datetime.now()
            created_at = now.strftime("%d.%m.%Y %H:%M:%S")

            add_event(
                description=description,
                event_date=now.strftime("%Y-%m-%d"),
                event_time=now.strftime("%H:%M:%S")
            )

            logger.info("Напоминание создано: '%s' (%s)", description, created_at)

            return {
                "success": True,
                "description": description,
                "created_at": created_at,
                "message": MSG_CREATED.format(description=description, created_at=created_at)
            }

        except Exception as e:
            logger.error("Ошибка при создании напоминания: %s", e, exc_info=True)
            return {"success": False, "message": MSG_CREATE_FAILED}

    # Gets all reminders from the database
    def get_all_reminders(self) -> dict:
        try:
            events = get_all_events()
            if events is None:
                raise ValueError("get_all_events() вернул None")

            logger.info("Успешно получено %d напоминаний.", len(events))

            lines = [f"{i}. {event['description']}" for i, event in enumerate(events, start=1)]
            message = "\n".join([MSG_LIST_HEADER, *lines]) if lines else MSG_LIST_EMPTY

            return {
                "success": True,
                "data": events,
                "count": len(events),
                "message": message
            }

        except Exception as e:
            logger.error("Ошибка при получении напоминаний: %s", e, exc_info=True)
            return {"success": False, "message": MSG_LIST_FAILED}
