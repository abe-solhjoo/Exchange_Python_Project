import requests
from config import URL, rules
import json
from datetime import datetime

from mail import send_smtp_email
from notification import send_sms


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
    for exc in rules['send_email']['currencies']:
        temp[exc] = new_rates[exc]
        print(temp)
    rates = temp

    subject = 'rates:' + str_date
    text = json.dumps(rates)

    send_smtp_email(subject, text)


def check_notify_rules(rates):
    currencies = rules['send_sms']['currencies']
    msg = ''
    for exc in currencies:
        if rates[exc] <= currencies[exc]['min']:
            msg += f'{exc} reached min: {rates[exc]} \n'
        if rates[exc] >= currencies[exc]['max']:
            msg += f'{exc} reached max: {rates[exc]} \n'
    return msg


def send_notification(msg):
    print(msg)
    send_sms(msg)


if __name__ == "__main__":
    rsp = get_rates()
    print(rsp)

    if rules['archive']:
        archive(rsp)

    if rules['send_email']['enable']:
        send_email(rsp)

    if rules['send_sms']['enable']:
        notification_msg = check_notify_rules(rsp['data'])
        if notification_msg:
            send_notification(notification_msg)
