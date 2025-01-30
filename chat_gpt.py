'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 30/01/2025
Ending //
'''
# Installing the necessary libraries
import requests
import os
from dotenv import load_dotenv
load_dotenv()


class ChatGPT:
    """AI is creating summary for
    """
    def __init__(self):
        # Retrieve the API key from environment variables
        self.api_key = os.getenv("GPT_API_KEY")
        # If the API key is not found, raise an error
        if not self.api_key:
            raise ValueError("Не найден API-ключ для ChadGPT. Проверьте .env файл.")

    def ask(self, message):
        """AI is creating summary for ask

        Args:
            message ([type]): [description]

        Returns:
            [type]: [description]
        """
        # Define the API endpoint URL
        url = "https://ask.chadgpt.ru/api/public/gpt-4o-mini"
        # Construct the request payload
        request_json = {
            "message": message,
            "api_key": self.api_key
        }

        try:
            # Send a POST request to the API
            response = requests.post(url, json=request_json)
            # Check if the response status code is not 200 (OK)
            if response.status_code != 200:
                return f"Ошибка при отправке запроса: {response.status_code}"
                # Parse the JSON response
            resp_json = response.json()
            # Check if the API response indicates success
            if resp_json.get("is_success"):
                resp_msg = resp_json.get("response", "Ошибка в ответе сервера")
                used_words = resp_json.get("used_words_count", 0)
                return f"{resp_msg} (потрачено слов: {used_words})"
            else:
                return f"Ошибка: {resp_json.get('error_message', 'Неизвестная ошибка')}"

        except Exception as e:
            # Handle any exceptions that may occur during the request
            return f"Ошибка при работе с нейросетью: {e}"
