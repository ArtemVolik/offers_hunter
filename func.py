import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable


def get_response(url, params=None):
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()


def get_languages():
    response = requests.get('https://habr.com/ru/post/310262/')
    response.raise_for_status()
    soup = BeautifulSoup(response.content, features='lxml')
    source_headers_raw = [header.text.replace(':', '').split() for header in soup.find_all('h3')[:15]]
    languages = {header[3] for header in source_headers_raw if "CSS" not in header if "Shell" not in header}
    return {language: dict() for language in languages}


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return int((salary_from + salary_to) / 2)
    if salary_from:
        return int(salary_from * 1.2)
    if salary_to:
        return int(salary_to * 0.8)


def print_table_from_data(title, data):
    table_data = [('Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата')]
    unpacked = [(language[0], *language[1].values()) for language in data.items()]
    for language_data in unpacked:
        table_data.append(language_data)
    table_instance = AsciiTable(table_data, title)
    table_instance.justify_columns[2] = 'right'
    print(table_instance.table)
    print()
