import urllib.request, urllib.error, urllib.parse
import http.cookiejar


def get(url):
    request = urllib.request.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:49.0) Gecko/20100101 Firefox/49.0')
    request.add_header('Referer', '')
    try:
        with urllib.request.urlopen(request) as response:
            data = response.read()
            print('Status:', response.status, response.reason)
            print('Data:', data.decode('utf-8'))
    except urllib.error.HTTPError as e:
        print('HTTPError:', end=' ')
        print(e.code, end=' ')
        print(e.reason)
    except urllib.error.URLError as e:
        print('URLError:', end=' ')
        print(e.reason)


if __name__ == '__main__':
    #get('http://httpbin.org/status/404')
    get('http://google.com/')
