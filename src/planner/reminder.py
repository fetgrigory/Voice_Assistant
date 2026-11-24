import logging
from datetime import datetime
from src.db.crud import add_event

logger = logging.getLogger(__name__)


class ReminderManager:
    # Creates a new note and saves it to the database
    def create_reminder(self, description: str) -> dict:
        description = (description or "").strip()
        if not description:
            return {
                "success": False,
                "message": "Текст напоминания пуст."
            }

        try:
            now = datetime.now()
            formatted = now.strftime("%d.%m.%Y %H:%M:%S")

            add_event(
                description=description,
                event_date=now.strftime("%Y-%m-%d"),
                event_time=now.strftime("%H:%M:%S")
            )

            logger.info("Напоминание создано: '%s' (%s)", description, formatted)

            return {
                "success": True,
                "description": description,
                "created_at": formatted,
                "message": f'Напоминание создано "{description}" создана от {formatted}.'
            }

        except Exception as e:
            logger.error("Ошибка при создании напоминания: %s", e, exc_info=True)
            return {
                "success": False,
                "message": "Не удалось создать напоминание. Попробуйте ещё раз."
            }
