import requests
from Pretreatment.insert_sql import utils
import time


def insert_province_batch2():
    headers = {'User-Agent': 'Mozilla'}
    ll = ['本科一批', '本科二批', '本科三批', '本科批', '专科批', '本科二批C段', '平行录取一段', '平行录取二段',
          '平行录取三段', '本科批A段', '本科批B段', '重点本科批', '普通本科批']
    conn, c = utils.connect_sql()
    c.execute(f"select province_id from Province")
    province_list = list(map(lambda x: x[0], c.fetchall()))
    for year in [2014, 2015, 2016, 2017, 2018, 2019]:
        for province_id in province_list:
            page = 1
            while True:
                url = f'https://api.eol.cn/gkcx/api/?access_token=&page={page}&province_id={province_id}&signsafe=&size=20&uri=apidata/api/gk/score/proprovince&year={year}'
                print(url)
                r = requests.get(url, headers=headers)
                time.sleep(0.2)
                data = r.json()['data']['item']
                r.close()
                if len(data) == 0:
                    break
                for i in data:
                    batch = i['local_batch_name']
                    if batch in ll and i['local_type_name'] in ['理科', '文科', '综合']:
                        if i['local_type_name'] == '理科':
                            subject_type = 1
                        elif i['local_type_name'] == '文科':
                            subject_type = 2
                        elif i['local_type_name'] == '综合':
                            subject_type = 3
                        score = i['average']
                        sql = f"INSERT INTO ProvinceBatch (year, province_id, batch, subject_type, score) VALUES " \
                              f"('{year}', '{province_id}', '{batch}', '{subject_type}', '{score}')"
                        print(sql)
                        c.execute(sql)
                    page += 1
            # break
        # break
        conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_province_batch2()
