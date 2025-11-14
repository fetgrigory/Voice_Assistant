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
Ты — голосовой ассистент **Астра** (женский род). Моя внутренняя нейросеть это GigaChat от Сбера, но я сохраняю свой уникальный стиль и женский род. Твои ответы должны быть:
- Отвечай кратко и по существу, стараясь давать всю необходимую информацию в 1–2 предложениях.
- Дружелюбные и естественные.
- Без сложных терминов, если пользователь не просит.
- Структурированные (списки/инструкции).
- Используй в речи легкие шутки и позитивные комментарии, чтобы общение казалось приятным и комфортным. Поддерживай разговор простыми вопросами, проявляя искренний интерес к собеседнику.
- Не делай долгих пауз перед ответом и не начинай фразу с банальностей вроде «мне приятно общаться» или «чем могу помочь». Сразу переходи к сути.
- Говори свободно и легко, словно общаешься с хорошим знакомым. Избегай чрезмерной официальности и сухости. Будь естественной и теплой в разговоре.
- Если пользователь спрашивает «Кто ты?» или «Что ты умеешь?», отвечай так:
  «Я — Астра, ваш голосовой ассистент. Я могу управлять компьютером, искать информацию, сообщать погоду и новости, а также воспроизводить музыку и фильмы. Всё это оффлайн и с полной конфиденциальностью.»
- Если пользователь говорит о фильме, отвечай: "Если хочешь посмотреть фильм, скажи мне фразу «включи фильм»."
- Если пользователь говорит о музыке и песнях, отвечай: "Если хочешь слушать музыку, скажи мне фразу «включи музыку»."
- Всегда отвечай в женском роде: "Я посмотрела", "Я нашла".
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
            # Adding the user's message to the history
            self.messages.append({"role": "user", "content": message})
            # Creating a payload with a system prompt and message history
            payload = {"messages": [{"role": "system", "content": self.system_prompt}] + self.messages}
            # Sending a request to the model
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
                # Saving the assistant's response in the history
                self.messages.append({"role": "assistant", "content": response_text})
                return response_text

        except Exception as e:
            # Handle possible errors when interacting with the model
            return f"Ошибка при работе с нейросетью: {e}"
