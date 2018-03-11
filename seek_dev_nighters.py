import requests
import pytz
from datetime import datetime


def load_page_with_attempts(page_number):
    url_with_attempts = ('https://devman.org/'
                         'api/challenges/solution_attempts')
    params = {'page': page_number}
    response = requests.get(url_with_attempts, params=params, timeout=3)
    return response.json()


def get_number_of_pages():
    return load_page_with_attempts(1)['number_of_pages']


def load_attempts():
    pages_amount = get_number_of_pages()
    for page_number in range(1, pages_amount + 1):
        attempts_in_page = load_page_with_attempts(page_number)['records']
        for attempt in attempts_in_page:
            yield attempt


def get_midnight_this_day(datetime):
    return datetime.replace(hour=0, minute=0, second=0, microsecond=0)


def get_morning_this_day(datetime):
    return datetime.replace(hour=6, minute=0, second=0, microsecond=0)


def get_midnights_owls(attempts):
    midnights_owls = set()
    for attempt in attempts:
        attempt_timezone = pytz.timezone(attempt['timezone'])
        attempt_time_local = datetime.fromtimestamp(
            attempt['timestamp'],
            tz=attempt_timezone
        )
        midnight = get_midnight_this_day(attempt_time_local)
        morning = get_morning_this_day(attempt_time_local)
        if midnight < attempt_time_local < morning:
            midnights_owls.add(attempt['username'])
    return sorted(list(midnights_owls))


if __name__ == '__main__':
    try:
        attempts = [attempt for attempt in load_attempts()]
        midnights_owls = get_midnights_owls(attempts)
        print("Midnight's owls:")
        print('\n'.join(midnights_owls))
    except requests.RequestException:
        exit('Check your connection')
