import requests
from pprint import pprint
from bs4 import BeautifulSoup

urls = {
    'specialization': 'https://api.hh.ru/specializations',
    'vacancies': 'https://api.hh.ru/vacancies'
}


def get_response(url, params=None):
    response = requests.get(url, params)
    response.raise_for_status()
    return response.json()


def get_specialization(url):
    specializations = get_response(url)
    programming_vacancy = [(item['name'], item['id']) for line in specializations for item in line['specializations'] \
                           if 'программирование' in item['name'].lower()]
    return programming_vacancy[0][1]


def get_programist_vacansies(url, language, page=''):
    params = dict()
    params['specialization'] = get_specialization(urls['specialization'])
    params['period'] = 30
    params['area'] = 1
    params['text'] = language
    params['per_page'] = 100
    if page:
        params['page'] = page
    return get_response(url, params=params)


def predict_salary(salary: dict):
    if salary['currency'] != 'RUR' or salary is None:
        return
    if salary['from'] and salary['to']:
        return int((salary['from'] + salary['to']) / 2)
    if salary['from']:
        return int(salary['from'] * 0.8)
    if salary['to']:
        return int(salary['to'] * 1.2)


response = requests.get('https://habr.com/ru/post/310262/')
response.raise_for_status()
soup = BeautifulSoup(response.content, features='lxml')
source_headers_raw = [header.text.replace(':', '').split() for header in soup.find_all('h3')[:15]]
languages = {header[3] for header in source_headers_raw if "CSS" not in header if "Shell" not in header}
program_languages = {language: dict() for language in languages}


for language in program_languages.keys():
    vacancies_all_pages = []
    pages_quantity = get_programist_vacansies(urls['vacancies'], language)['pages']
    vacancies_all_pages = [get_programist_vacansies(urls['vacancies'], language, page) for page in range(pages_quantity)]
    vacancies_found = 0
    salaries_sum = 0
    processed_vacancy_count = 0
    for page in vacancies_all_pages:
        vacancies_found += page['found']
        page_predicted_salaries = [predict_salary(vacansy['salary']) for vacansy in page['items'] if vacansy['salary']]
        page_salaries = [salary for salary in page_predicted_salaries if salary is not None]
        salaries_sum += sum(page_salaries)
        processed_vacancy_count += len(page_salaries)
    program_languages[language]['vacancies_found'] = vacancies_found
    program_languages[language]['avarage_salary'] = int(salaries_sum / processed_vacancy_count)
    program_languages[language]["vacancies_processed"] = processed_vacancy_count

pprint(program_languages)





