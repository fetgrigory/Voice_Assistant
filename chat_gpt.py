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
            # Make a request to the GPT4Free API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": message}],
                web_search=False  # Disable web search if not needed
            )
            return self.process_content(response.choices[0].message.content)
        except Exception as e:
            # Handling possible errors when making a request to the API
            return f"Ошибка при работе с нейросетью: {e}"
