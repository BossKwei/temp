import re
import requests


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
resources = {'1': [['http://www.xicidaili.com/nn/{}', 1, 10, r'<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>'],
                   ['http://www.xicidaili.com/nt/{}', 1, 10, r'<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>'],
                   ['http://www.xicidaili.com/wn/{}', 1, 10, r'<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>'],
                   ['http://www.xicidaili.com/wt/{}', 1, 10, r'<td>(\d+\.\d+\.\d+\.\d+)</td>\s+<td>(\d+)</td>']]}
results = []


def main():
    for idx in resources:
        for url, left, right, pattern in resources[idx]:
            for i in range(left, right):
                response = requests.get(url.format(i), headers=headers)
                for m in re.finditer(pattern, response.text):
                    results.append(m.groups())
    print(results)
    return results


if __name__ == '__main__':
    main()
