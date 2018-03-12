import requests
import pytz
from datetime import datetime


def fetch_page_with_attempts(page_number):
    url_with_attempts = ('https://devman.org/'
                         'api/challenges/solution_attempts')
    params = {'page': page_number}
    response = requests.get(url_with_attempts, params=params, timeout=3)
    return response.json()


def load_attempts():
    page_number = 1
    while True:
        response = fetch_page_with_attempts(page_number)
        attempts_in_page = response['records']
        for attempt in attempts_in_page:
            yield attempt
        number_of_pages = response['number_of_pages']
        page_number += 1
        if page_number > number_of_pages:
            break


def get_midnights_owls(attempts):
    midnights_owls = set()
    midnight = 0
    morning = 6
    for attempt in attempts:
        attempt_timezone = pytz.timezone(attempt['timezone'])
        attempt_time_local = datetime.fromtimestamp(
            attempt['timestamp'],
            tz=attempt_timezone
        )
        if midnight <= attempt_time_local.hour < morning:
            midnights_owls.add(attempt['username'])
    return sorted(list(midnights_owls))


if __name__ == '__main__':
    try:
        midnights_owls = get_midnights_owls(load_attempts())
        print("Midnight's owls:")
        print('\n'.join(midnights_owls))
    except requests.RequestException:
        exit('Check your connection')
