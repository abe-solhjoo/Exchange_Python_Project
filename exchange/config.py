URL = 'https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_NBme7MmmUaYzaBCjQ5ItXHIf14nGBP68jGjTWaVk'


# rules = {
#     'archive': True,
#     'send_email': True,
#     # 'currencies': None,
#     'currencies': ['USD', 'AUD', 'BGN']
# }

rules = {
    'archive': True,
    'send_email': {
        'email_receiver': '',
        'enable': False,
        'currencies': ['USD', 'AUD', 'BGN']
    },
    'send_sms': {
        'sms_receiver': '',
        'enable': True,
        'currencies': {
            'USD': {'min': 1, 'max': 2}
        }
    }
}