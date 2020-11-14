import requests
import os
from dotenv import load_dotenv
from HeadHunter import predict_salary, get_languages, print_table_from_data

url = 'https://api.superjob.ru/2.33/vacancies/'


def main():
    load_dotenv()
    token = os.getenv('SUPER_JOB_TOKEN')
    header = {'X-Api-App-Id': token}
    programing_languages = get_languages('https://habr.com/ru/post/310262/')
    params = {
        'town': 4,
        'catalogues': 48,
        'page': '',
        'count': '100'
    }
    for language in programing_languages:
        params['page'] = 0
        vacancies_found = 0
        vacancies_operated = 0
        salaries_sum = 0
        params['keywords'] = f'Программист {language}'
        more_pages = True
        while more_pages:
            response = requests.get(url, headers=header, params=params)
            params['page'] += 1
            response.raise_for_status()
            content = response.json()
            more_pages = content['more']
            vacancies_found += content['total']
            vacancies = content['objects']
            predicted_salaries = [predict_salary(vacancy['payment_from'], vacancy['payment_to']) for vacancy in
                                  vacancies
                                  if predict_salary(vacancy['payment_from'], vacancy['payment_to']) is not None]
            vacancies_operated += len(predicted_salaries)
            salaries_sum = sum(predicted_salaries)

        programing_languages[language].update({
            'vacancies_found': vacancies_found,
            'vacancies_processed': vacancies_operated,
            'average_salary': int(salaries_sum / vacancies_operated if vacancies_operated else 1)

        })
    return programing_languages


if __name__ == '__main__':
    programing_languages_statistic = main()
    print_table_from_data('SuperJob Moscow', programing_languages_statistic)
