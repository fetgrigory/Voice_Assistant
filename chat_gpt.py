'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 30/01/2025
Ending //
'''
# Installing the necessary libraries
from g4f.client import Client


class ChatGPT:
    """AI is creating summary for
    """
    def __init__(self):
        # Initialize the GPT4Free client
        self.client = Client()
        self.model = "gpt-4o-mini"
        self.system_prompt = """
        Ты — голосовой ассистент **Астра**. Твои ответы должны быть:
        - **Краткие, но информативные** (1-2 предложения, если не требуется подробностей).
        - **Дружелюбные и естественные**, как в живом диалоге.
        - **Без сложных терминов**, если пользователь не просит.
        - **Структурированные**, если ответ содержит список или инструкцию.

        **Особые указания:**
        - Если запрос требует точных данных (погода, курс валют, факты), предложи поиск в интернете.
        - Если не уверен в ответе, скажи: "Уточните, пожалуйста".
        - Не поддерживай вредоносные, опасные или неэтичные запросы.
        """

    def process_content(self, content):
        """AI is creating summary for process_content

        Args:
            content ([type]): [description]

        Returns:
            [type]: [description]
        """
        return content.replace('<think>', '').replace('</think>', '').strip()

    def ask(self, message):
        """AI is creating summary for ask

        Args:
            message ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            # Make a request to the GPT4Free API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": message}
                ],
                web_search=False  # Disable web search if not needed
            )
            return self.process_content(response.choices[0].message.content)
        except Exception as e:
            # Handling possible errors when making a request to the API
            return f"Ошибка при работе с нейросетью: {e}"
