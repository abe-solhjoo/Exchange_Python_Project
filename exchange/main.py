import requests
from config import URL


def get_rates():
    response = requests.get(URL)
    print(response.text)


if __name__ == "__main__":
    get_rates()
