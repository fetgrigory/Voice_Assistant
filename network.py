'''
This module make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/11/2024
Ending //
'''
import wikipedia
import webbrowser as wb

class NetworkActions:
    def web_search(self, query):
        if query:
            wb.open("https://www.google.ru/search?q=" + query)
            return "Ищу информацию по запросу " + query
        else:
            return "Я не поняла, что надо искать."

    def wikipedia_search(self, query):
        try:
            wikipedia.set_lang("ru")
            query = query.replace("википедия", "").strip()
            wiki_result = wikipedia.summary(query, sentences=2)
            print(f"По данным русской википедии: {wiki_result}")
            return wiki_result
        except wikipedia.exceptions.PageError:
            return "Информация по запросу не найдена в Википедии."
        except wikipedia.exceptions.DisambiguationError:
            return "Найдено несколько вариантов, уточните запрос."
        except Exception as e:
            return "Я не поняла, что надо искать в Википедии."

    def check_searching(self, query):
        if any(word in query for word in ["найди", "найти"]):
            query = query.replace("найди", "").replace("найти", "").strip()
            return self.web_search(query)
        elif "википедия" in query:
            return self.wikipedia_search(query)
        else:
            return False
