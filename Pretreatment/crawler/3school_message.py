import requests
import pandas as pd


def main():
    headers = {'User-Agent': 'Mozilla/5.0'}
    df = pd.DataFrame()
    for page in range(1, 145+1):
        print(page)
        url = f'https://api.eol.cn/gkcx/api/?access_token=&keyword=&page={page}&province_id=&school_type=&signsafe=&size=20&sort=view_total&sorttype=desc&type=&uri=apidata/api/gk/school/lists'
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            lis = r.json()['data']['item']
            for d in lis:
                add_df = pd.DataFrame([d])
                df = pd.concat([df, add_df])
        else:
            print(f'page: {page} error')
    df.to_csv('../result/school.csv', index=None)


if __name__ == '__main__':
    main()
