import time
import re
import json
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5'
                          '37.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'),
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en;q=0.9'}


def parse_1():
    response = requests.get('https://api.coinmarketcap.com/v1/ticker/?limit=0', headers=HEADERS)
    response.raise_for_status()
    return json.loads(response.text)


def parse_2(currency_id):
    source_url = 'unknown'
    for step in range(10):
        try:
            url = 'https://coinmarketcap.com/currencies/{id}/'.format(id=currency_id)
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            source_url = re.search(r'<a href="(https://github.com/\S+)" target="_blank">Source Code</a>',
                                   response.text).group(1)
            break
        except AttributeError:
            break
        except Exception as e:
            print(currency, type(e), e)
        time.sleep(30)
    return source_url


if __name__ == '__main__':
    currencies_list = parse_1()
    for idx, currency in enumerate(currencies_list):
        currency_github = parse_2(currency['id'])
        currencies_list[idx]['github'] = currency_github
        print(idx, currency)
        time.sleep(0.2)
    #
    print(json.dumps(currencies_list))
