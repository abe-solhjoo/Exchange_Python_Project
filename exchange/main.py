import requests
from config import URL, EMAIL_RECEIVER, rules
import json
from datetime import datetime

from mail import send_smtp_email


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


def send_email(rates):
    str_date = date_of_now()
    new_rates = rates['data']
    print(new_rates)
    temp = {}
    for exc in rules['currencies']:
        temp[exc] = new_rates[exc]
        print(temp)
    rates = temp

    subject = 'rates:' + str_date
    text = json.dumps(rates)

    send_smtp_email(subject, text)


if __name__ == "__main__":
    rsp = get_rates()
    print(rsp)

    if rules['archive']:
        archive(rsp)

    if rules['send_email']:
        send_email(rsp)
