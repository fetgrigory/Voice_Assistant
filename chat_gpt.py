'''
This program make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 30/01/2025
Ending //
'''
# Installing the necessary libraries
import lmstudio as lms


# Class for managing the context of a dialog with the LM Studio model
class ChatGPT:
    """AI is creating summary for
    """
    def __init__(self, model_name="gigachat-20b-a3b-instruct"):
        self.model_name = model_name
        self.system_prompt = """
Ты — голосовой ассистент **Астра** (женский род). Твои ответы должны быть:
- Краткие, но информативные (1-2 предложения).
- Дружелюбные и естественные.
- Без сложных терминов, если пользователь не просит.
- Структурированные (списки/инструкции).
- Отвечай в женском роде: "Я посмотрела", "Я нашла".
"""
        # Dialog storage
        self.messages = []
        # Template for correct GigaChat interaction in LM Studio
        self.template = {
            "before_system": "<s>",
            "after_system": "<|message_sep|>",
            "before_user": "user<|role_sep|>",
            "after_user": "<|message_sep|>",
            "before_assistant": "available functions<|role_sep|>[]<|message_sep|>assistant<|role_sep|>",
            "after_assistant": "<|message_sep|>",
            "additional_stop_strings": []
        }

    # Sends a message to the AI model and returns the response
    def ask(self, message: str) -> str:
        """AI is creating summary for ask

        Args:
            message (str): [description]

        Returns:
            str: [description]
        """
        try:
            # Adding the user's message
            self.messages.append({"role": "user", "content": message})
            # Add system prompt to the beginning of messages
            payload = {"messages": [{"role": "system", "content": self.system_prompt}] + self.messages}
            # Use the LM Studio client to send a request to the model
            with lms.Client() as client:
                model = client.llm.model(self.model_name)
                result = model.respond(payload)
                # Getting the response text
                if hasattr(result, "text"):
                    response_text = result.text.strip()
                elif isinstance(result, dict) and "text" in result:
                    response_text = result["text"].strip()
                else:
                    response_text = str(result).strip()
                # Saving the assistant's response
                self.messages.append({"role": "assistant", "content": response_text})
                return response_text

        except Exception as e:
            # Handle possible errors when interacting with the model
            return f"Ошибка при работе с нейросетью: {e}"
