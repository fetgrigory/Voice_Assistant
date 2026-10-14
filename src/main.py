import os
import logging
from src.core.assistant_core import Assistant

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/assistant.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

if __name__ == "__main__":
    assistant = Assistant()
