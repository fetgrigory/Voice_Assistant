'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 30/01/2025
Ending //
'''
# Installing the necessary libraries
from openai import OpenAI
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

        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1/chat/completions",
            api_key=self.api_key,
        )
        self.model = "deepseek/deepseek-r1"

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
        try:
            completion = self.client.chat.completions.create(
                extra_body={},
                model=self.model,
                messages=[{"role": "user", "content": message}]
            )
            return self.process_content(completion.choices[0].message.content)
        except Exception as e:
            # Handling possible errors when making a request to the API
            return f"Ошибка при работе с нейросетью: {e}"