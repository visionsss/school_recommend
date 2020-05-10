import requests
import pandas as pd


def scrape_api(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    return r


def save(r, school_id):
    with open(f'../result/school_detail/{school_id}.txt', 'w', encoding='utf-8') as f:
        f.write(str(r.json()))


def main():
    for i in range(29, 4000):
        url = f'https://static-data.eol.cn/www/2.0/school/{i}/info.json'
        r = scrape_api(url)
        print(i, end=' ')
        if r.status_code == 200:
            r.encoding = 'utf-8'
            data = r.json()['data']
            school_id = data['school_id']
            save(r, school_id)
            print(data['school_id'], data['name'], data['province_id'])


if __name__ == '__main__':
    main()