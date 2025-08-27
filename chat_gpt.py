'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 30/01/2025
Ending //
'''
# Installing the necessary libraries
import lmstudio as lms


class ChatGPT:
    """AI is creating summary for
    """
    def __init__(self, model_name="google/gemma-3-12b"):
        self.model_name = model_name
        self.system_prompt = """
Ты — голосовой ассистент **Астра** (женский род). Твои ответы должны быть:
- Краткие, но информативные (1-2 предложения).
- Дружелюбные и естественные.
- Без сложных терминов, если пользователь не просит.
- Структурированные (списки/инструкции).
- Отвечай в женском роде: "Я посмотрела", "Я нашла".
"""

    # Sends a message to the AI model and returns the response
    def ask(self, message: str) -> str:
        """AI is creating summary for ask

        Args:
            message (str): [description]

        Returns:
            str: [description]
        """
        try:
            # Use the LM Studio client to send a request to the model
            with lms.Client() as client:
                model = client.llm.model(self.model_name)
                result = model.respond(
                    f"{self.system_prompt}\nПользователь: {message}\nАстра:"
                )
                # Extract the text if the result has a text attribute
                if hasattr(result, "text"):
                    return result.text.strip()
                return str(result).strip()
        except Exception as e:
            # Handle possible errors when interacting with the model
            return f"Ошибка при работе с нейросетью: {e}"
