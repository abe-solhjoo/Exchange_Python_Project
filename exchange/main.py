import requests
from khayyam import JalaliDatetime

from config import URL, rules
import json
from datetime import datetime

from mail import send_smtp_email
from notification import send_sms
from esb_sms import send_sms_ESB


def get_rates():
    """
    get currencies rates from api
    :return: rates in json
    """
    response = requests.get(URL)
    if response.status_code == 200:
        return json.loads(response.text)
    return response.status_code


def archive(rates):
    """
    archive rates in archive dir in json file
    :param rates: rate from api
    :return: null
    """
    en_time, jalali_time = date_of_now()
    with open(f'archive/{en_time}.json', 'w') as f:
        f.write(json.dumps(rates))
    print(jalali_time)


def date_of_now():
    """
    create date of now in str type
    :return: Jalali time and Miladi time
    """
    now = datetime.now()
    # str_time = f'{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}'
    str_time = now.strftime('%Y-%m-%d %H.%M.%S')
    jalali_time = JalaliDatetime(now)
    jalali_time = jalali_time.strftime('%Y-%m-%d %H.%M.%S')
    return str_time, jalali_time


def send_email(rates):
    """
    base on config file, call methods for send email
    :param rates: rate from api
    :return: email
    """
    str_date, jalali_date = date_of_now()
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
    """
    check conditions for send sms
    :param rates: rates from api
    :return: message
    """
    currencies = rules['send_sms']['currencies']
    msg = ''
    for exc in currencies:
        if rates[exc] <= currencies[exc]['min']:
            msg += f'{exc} reached min: {rates[exc]} \n'
        if rates[exc] >= currencies[exc]['max']:
            msg += f'{exc} reached max: {rates[exc]} \n'
    return msg


def send_notification(msg):
    """
    base on config file, choose server for send sms
    :param msg: test of message
    :return: null
    """
    print(msg)
    servers = rules['send_sms']['servers']
    if servers['Kavenegar']:
        send_sms(msg)
    if servers['ESB']:
        send_sms_ESB(msg)


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
