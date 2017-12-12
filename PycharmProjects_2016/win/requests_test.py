import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0'}
payload = {'key1': 'value1', 'key2': 'value2'}

# Make a request
try:
    # r = requests.get('http://httpbin.org/get', params=payload, headers=headers, timeout=(3.05, 8.0))
    # r = requests.get('http://www.cqu.edu.cn/', params=payload, headers=headers, timeout=(3.05, 8.0))
    r = requests.get('http://httpbin.org/status/503', params=payload, headers=headers, timeout=(3.05, 8.0))
    r.raise_for_status()

    # Print out the response
    print('HTTP Status:', end=' ')
    print(r.status_code, end=' ')
    print(r.reason)

    # Other testing
    print('Encoding:', end=' ')
    print(r.encoding)

    #
    # print(r.history)
    # print(r.content)
    # print(r.text)
    # print(r.headers)

except requests.RequestException as e:
    for x in e.args:
        print(x)
