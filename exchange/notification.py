from kavenegar import *

from config import rules
from local_config import Kavenegar_API_key


def send_sms(text):
    try:
        api = KavenegarAPI(Kavenegar_API_key)
        params = {
            'sender': '1000689696',
            'receptor': rules['send_sms']['sms_receiver'],
            'message': text
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)