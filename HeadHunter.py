from func import get_response, get_languages, predict_salary, print_table_from_dict

urls = {
    'specialization': 'https://api.hh.ru/specializations',
    'vacancies': 'https://api.hh.ru/vacancies'
}


def get_specialization(url, specialization):
    specializations = get_response(url)
    programming_vacancy = [(item['name'], item['id']) for line in specializations for item in line['specializations']
                           if specialization in item['name'].lower()]
    return programming_vacancy[0][1]


def get_programmer_vacancies(url, language, page=''):
    params = dict()
    params['specialization'] = get_specialization(urls['specialization'], 'программирование')
    params['period'] = 30
    params['area'] = 1
    params['text'] = language
    params['per_page'] = 100
    if page:
        params['page'] = page
    return get_response(url, params=params)


def main():
    program_languages = get_languages('https://habr.com/ru/post/310262/')
    for language in program_languages.keys():

        pages_quantity = get_programmer_vacancies(urls['vacancies'], language)['pages']
        vacancies_all_pages = [get_programmer_vacancies(urls['vacancies'], language, str(page)) for page in
                               range(pages_quantity)]
        vacancies_found: int = 0
        salaries_sum: int = 0
        processed_vacancy_count: int = 0

        for page in vacancies_all_pages:
            vacancies_found += page['found']
            page_predicted_salaries = [predict_salary(vacancy['salary']['from'], vacancy['salary']['to'])
                                       if vacancy['salary']['currency'] == 'RUR' else None for vacancy in page['items']
                                       if vacancy['salary'] is not None]
            page_salaries = [salary for salary in page_predicted_salaries if salary is not None]
            salaries_sum += sum(page_salaries)
            processed_vacancy_count += len(page_salaries)

        program_languages[language].update({
            'vacancies_found': vacancies_found,
            'vacancies_processed': processed_vacancy_count,
            'average_salary': int(salaries_sum / processed_vacancy_count)
        })
    return program_languages


if __name__ == '__main__':
    program_languages_statistic = main()
    print_table_from_dict('HeadHunter Moscow', program_languages_statistic)
