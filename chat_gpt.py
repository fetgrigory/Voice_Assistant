'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 30/01/2025
Ending //
'''
# Installing the necessary libraries
from ollama import pull, chat, ChatResponse, show

# Define the model name. This specifies which ChatGPT to use
MODEL_NAME = 'infidelis/GigaChat-20B-A3B-instruct-v1.5:q8_0'


class ChatGPT:
    """AI is creating summary for
    """

    def __init__(self):
        try:
            # Check if the model is already installed
            show(MODEL_NAME)
            print(f"✅ Модель {MODEL_NAME} уже установлена.")
        except Exception:
            # Download the model if not found
            print(f"📥 Модель {MODEL_NAME} не найдена. Начинается загрузка...")
            pull(MODEL_NAME)
            print(f"✅ Модель {MODEL_NAME} успешно загружена.")

    def ask(self, message):
        """AI is creating summary for ask

        Args:
            message ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            # Send a message to ChatGPT and get a response
            response: ChatResponse = chat(
                model=MODEL_NAME, messages=[{"role": "user", "content": message}]
            )
            # Return the AI-generated response
            return response.message.content
        except Exception as e:
            # Handle any exceptions that may occur during the request
            return f"Ошибка при работе с нейросетью: {e}"
