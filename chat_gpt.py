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
            raise ValueError("Не найден API-ключ для ChatGPT. Проверьте .env файл.")

        self.model = "deepseek/deepseek-r1"
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def process_content(self, content):
        """AI is creating summary for process_content

        Args:
            content ([type]): [description]

        Returns:
            [type]: [description]
        """
        return content.replace('<think>', '').replace('</think>', '')

    def ask(self, message):
        """AI is creating summary for ask

        Args:
            message ([type]): [description]

        Returns:
            [type]: [description]
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": message}],
            "stream": False
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            # Check if the response status code is not 200 (OK)
            if response.status_code != 200:
                return f"Ошибка при отправке запроса: {response.status_code}"
                # Parse the JSON response
            response_json = response.json()
            if "choices" in response_json:
                content = response_json["choices"][0]["message"].get("content", "")
                return self.process_content(content)
            else:
                return "Ошибка в ответе сервера."
        except Exception as e:
            # Handle any exceptions that may occur during the request
            return f"Ошибка при работе с нейросетью: {e}"