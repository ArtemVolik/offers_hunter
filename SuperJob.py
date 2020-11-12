import requests
from pprint import pprint
from HeadHunter import predict_salary, get_languages
import time

header = {'X-Api-App-Id': ''}
url = 'https://api.superjob.ru/2.33/vacancies/'
params = {
            'keywords': ['Программист', 'PHP'],
            'town': 4,
            'catalogues': [48],
            'page': '',
            'count': '100'
}

programing_languages = get_languages('https://habr.com/ru/post/310262/')
params = dict()
params['town'] = 4
params['catalogues'] = 48
params['count'] = 100
print(programing_languages)

for language in programing_languages:
    params['page'] = 0
    time.sleep(3)
    print(language)
    vacancies_found = 0
    vacancies_operated = 0
    salaries_sum = 0
    params['keywords'] = f'Программист {language}'
    print(params)
    more_pages = True
    print(params['page'])
    while more_pages:
        time.sleep(3)
        response = requests.get(url, headers=header, params=params)
        params['page'] += 1
        print(params['page'])
        response.raise_for_status()
        content = response.json()
        more_pages = content['more']
        print(more_pages)
        vacancies_found += content['total']
        print('total', content['total'])
        vacancies = content['objects']
        predicted_salaries = [predict_salary(vacancy['payment_from'], vacancy['payment_to']) for vacancy in vacancies
                              if predict_salary(vacancy['payment_from'], vacancy['payment_to']) is not None]
        vacancies_operated += len(predicted_salaries)
        salaries_sum = sum(predicted_salaries)

    programing_languages[language].update({
            'vacancies_found': vacancies_found,
            'avarage_salary': int(salaries_sum / vacancies_operated if vacancies_operated else 1),
            'vacancies_processed': vacancies_operated
        })

print(programing_languages)





