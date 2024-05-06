import requests
from config import rules
from local_config import ESB_Authorization, ESB_path

def send_sms_ESB(text):
    request_data = {
        "recipient": rules['send_sms']['sms_receiver'],
        "body": text
    }
            
    res = requests.post(ESB_path,
                        json=request_data,
                        headers={'Authorization': ESB_Authorization})
    


