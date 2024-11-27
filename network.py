import webbrowser as wb
import wikipedia


def web_search(query):
    wb.open('https://www.google.ru/search?q=' + query)
    # Returning the text for voice-over
    return 'Ищу информацию по запросу ' + query


def wikipedia_search(query):
    try:
        # Setting the language to Russian
        wikipedia.set_lang("ru")
        # Removing the word "wikipedia" from the query
        query = query.replace("википедия", "").strip()
        # We use the Wikipedia API to get information
        wiki_result = wikipedia.summary(query, sentences=2)
        print(f"Информация из Википедии: {wiki_result}")
        # Returning the text for voice-over
        return wiki_result
    except wikipedia.exceptions.PageError:
        return "Информация по запросу не найдена в Википедии."
    except wikipedia.exceptions.DisambiguationError:
        return "Найдено несколько вариантов, уточните запрос."


def check_seardhing(query):
    if "найди" in query:
        query = query.replace("найди", "").strip()
        return web_search(query)
    elif "найти" in query:
        query = query.replace("найти", "").strip()
        return web_search(query)
    elif "википедия" in query:
        return wikipedia_search(query)
    else:
        return False
    return True
