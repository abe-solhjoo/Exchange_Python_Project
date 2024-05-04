import requests
from config import URL
import json
from datetime import datetime


def get_rates():
    response = requests.get(URL)
    if response.status_code == 200:
        return json.loads(response.text)
    return response.status_code


def archive(rates):
    with open(f'archive/{date_of_now()}.json', 'w') as f:
        f.write(json.dumps(rates))


def date_of_now():
    now = datetime.now()
    str_time = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}'
    return str_time


if __name__ == "__main__":
    rsp = get_rates()
    print(rsp)
    archive(rsp)
