import requests
import pandas as pd


def scrap(page):
    url = f'https://api.eol.cn/gkcx/api/?access_token=&keyword=&level1=&level2=&page={page}&signsafe=&size=20&uri=apidata/api/gk/special/lists'
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    return r


def main():
    all_data = []
    for i in range(1, 73+1):
        r = scrap(i)
        if r.status_code == 200:
            data = r.json()['data']['item']
            for one in data:
                keys = list(one.keys())
                values = list(one.values())
                all_data.append(values)
                print(len(values), values)
    df = pd.DataFrame(all_data, columns=keys)
    df.to_csv('../result/special.csv')


if __name__ == '__main__':
    main()
