import time
import json
import re
import requests


HEADERS = {'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5'
                          '37.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'),
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en;q=0.9'}


def main():
    with open('coins_1.json', encoding='utf-8') as f:
        coins_data_1 = json.load(f)
    coins_data_2 = {}
    for item in coins_data_1:
        while True:
            try:
                time.sleep(10)
                github = item['github']
                github = github.rstrip('/')
                if github == 'unknown':
                    break
                _, path = github.split('://')
                m = re.findall('/', path)
                total_commits = 0
                if len(m) == 1:  # org
                    domain, org = path.split('/')
                    response = requests.get(github, auth=('bosskwei', 'decf692825aa28518d7af338a1d8f1007af82a01'))
                    response.raise_for_status()
                    m1 = re.findall('<a href="(\S+)" class="text-bold">', response.text)
                    m2 = re.findall('<a href="(\S+)" itemprop="name codeRepository">', response.text)
                    m = m1 + m2
                    for mm in m:
                        mm = mm.rstrip('/')
                        mm = mm.lstrip('/')
                        org, project = mm.split('/')
                        response = requests.get('https://api.github.com/repos/{0}/{1}/stats/contributors'.format(org, project), auth=('bosskwei', 'decf692825aa28518d7af338a1d8f1007af82a01'))
                        response.raise_for_status()
                        data_contributors = json.loads(response.text)
                        for c in data_contributors:
                            total_commits += c['total']
                elif len(m) == 2:  # resp
                    domain, org, project = path.split('/')
                    response = requests.get('https://api.github.com/repos/{0}/{1}/stats/contributors'.format(org, project), auth=('bosskwei', 'decf692825aa28518d7af338a1d8f1007af82a01'))
                    response.raise_for_status()
                    data_contributors = json.loads(response.text)
                    for c in data_contributors:
                        total_commits += c['total']
                print(github, total_commits)
                coins_data_2[github] = total_commits
                break
            except ValueError as e:
                print(e)
                time.sleep(60)
                break
            except requests.RequestException as e:
                print(e)
                time.sleep(60)
    print(json.dumps(coins_data_2))


if __name__ == '__main__':
    main()