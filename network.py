'''
This module make
Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/11/2024
Ending //
'''
import webbrowser as wb


def web_search(query):
    wb.open('https://www.google.ru/search?q=' + query)
    print('Ищу информацию по запросу ' + query)


def check_seardhing(query):
    if "найди" in query:
        query = query.replace("найди", "").strip()
        web_search(query)
    elif "найти" in query:
        query = query.replace("найти", "").strip()
        web_search(query)
    else:
        return False
    return True
