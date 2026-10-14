import logging
import webbrowser as wb
import feedparser
import requests
from bs4 import BeautifulSoup
from src.services.film_service import FilmManager
from src.services.music_service import MusicManager

logger = logging.getLogger(__name__)


# Handles weather-related operations
class WeatherService:
    # Get weather for specified city
    @staticmethod
    def get_weather(city: str) -> str:
        try:
            url = f"http://wttr.in/{city}"
            params = {'format': 3}
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.text.strip()
            return f"Ошибка: не удалось получить данные (код {response.status_code})."
        except Exception as e:
            return f"Ошибка при получении данных о погоде: %s" % e


# Handles news-related operations
class NewsService:
    def __init__(self, rss_url="https://russian.rt.com/rss", news_count=5):
        self.rss_url = rss_url
        self.news_count = news_count

    # Clean HTML tags from text
    @staticmethod
    def clean_html_text(text):
        if not text:
            return ""
        soup = BeautifulSoup(text, "html.parser")
        for a in soup.find_all("a"):
            if "Читать далее" in a.get_text():
                a.decompose()
        return ' '.join(soup.get_text(separator=" ", strip=True).split())

    # Fetch latest news from RSS feed
    def get_latest_news(self):
        try:
            feed = feedparser.parse(self.rss_url)
            if not feed.entries:
                logger.warning("No news entries found in RSS feed")
                return None

            return [
                {
                    'title': self.clean_html_text(entry.get('title', 'Без заголовка')),
                    'summary': self.clean_html_text(
                        entry.get('summary', entry.get('description', 'Нет описания'))
                    )
                }
                for entry in feed.entries[:self.news_count]
            ]
        except Exception as e:
            logger.error("Failed to fetch news: %s", e)
            return None


# Handles web search operations
class WebSearchService:
    # Perform web search
    @staticmethod
    def web_search(query):
        
        if query:
            wb.open("https://duckduckgo.com/?q=" + query)
            return "Ищу информацию по запросу " + query
        else:
            return "Я не поняла, что надо искать."

    # Open specified URL in browser
    @staticmethod
    def open_url(url):
        try:
            wb.open(url)
            return f"Открываю сайт: {url}"
        except Exception as e:
            return f"Ошибка при открытии сайта: %s" % e

        # Voice-activated search_online
    def search_online(self, tts, speech_recognizer):
        tts.speak("Что нужно найти в интернете?")
        query = speech_recognizer.listen_command()
        if query:
            result = self.web_search(query)
            logger.info("search_online query: %s, result: %s", query, result)
            tts.speak(result)
        else:
            tts.speak("Не удалось распознать запрос.")
            logger.warning("search_online: не удалось распознать запрос")


# Orchestrates all network-related operations
class NetworkActions:
    def __init__(self):
        self.music_player = MusicManager()
        self.film_player = FilmManager()
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.web_search_service = WebSearchService()

    # Get weather for specified city
    def get_weather(self, city):
        return self.weather_service.get_weather(city)

    # Get latest news
    def get_latest_news(self):
        return self.news_service.get_latest_news()

    # Open specified URL
    def open_url(self, url):
        return self.web_search_service.open_url(url)
