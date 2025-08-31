'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/11/2024
Ending //
'''
# Installing the necessary libraries
import os
import logging
from assistant_core import Assistant
# Create a logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)
# Configure logging
logging.basicConfig(
    filename='logs/assistant.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

if __name__ == "__main__":
    assistant = Assistant()
    assistant.main()
