'''
This module make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/11/2024
Ending //
'''
# Installing the necessary libraries
import webbrowser as wb
import os
import requests
from dotenv import load_dotenv
load_dotenv()


class NetworkActions:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    # Performs a web search using Google
    def web_search(self, query):
        """AI is creating summary for web_search

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        if query:
            # Opens the Google search URL with the provided query
            wb.open("https://www.google.ru/search?q=" + query)
            # Returns a confirmation message
            return "Ищу информацию по запросу " + query
        else:
            # Returns an error message for empty queries
            return "Я не поняла, что надо искать."

    # Checks the query string to determine the appropriate search method (web only)
    def check_searching(self, query):
        """AI is creating summary for check_searching

        Args:
            query ([type]): [description]

        Returns:
            [type]: [description]
        """
        # Checks if the query contains words like "найди" or "найти", indicating a web search
        if any(word in query for word in ["найди", "найти"]):
            # Removes the keywords
            query = query.replace("найди", "").replace("найти", "").strip()
            # Performs a web search
            return self.web_search(query)
        else:
            return False

# Getting weather information
    def get_weather(self, city):
        """AI is creating summary for get_weather

        Args:
            city ([type]): [description]

        Returns:
            [type]: [description]
        """
        open_weather_token = os.getenv("OPEN_WEATHER_TOKEN")
        if not open_weather_token:
            return "Ошибка: не задан токен для OpenWeather."

        try:
            r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru")

            data = r.json()

            if data.get("cod") != 200:
                return f"Ошибка: {data.get('message', 'не удалось получить данные о погоде')}."

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            weather = data["weather"][0]["description"]

            return f"Сейчас в городе {city}: {weather}, температура {temp}°C, ощущается как {feels_like}°C."
        except Exception as e:
            return f"Ошибка при получении данных о погоде: {e}"
