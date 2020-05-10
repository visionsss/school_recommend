import requests
from Pretreatment.insert_sql import utils


def clean_data(s: str):
    res = []
    li = ['理科', '文科', '综合']
    for i in li:
        if i in s:
            res.append(i)
    return res


def clean_batch_data(s: set):
    ll = ['本科一批', '本科二批', '本科三批', '本科批', '专科批', '本科二批C段', '平行录取一段', '平行录取二段',
          '平行录取三段', '本科批A段', '本科批B段', '重点本科批', '普通本科批']
    li = set()
    for i in ll:
        li.add(i)
    return s.__and__(li)


def insert_province_batch():
    conn, c = utils.connect_sql()
    url = 'https://static-data.eol.cn/www/config/dicprovince/province_control.json'
    r = requests.get(url)
    all_data = r.json()
    years = all_data['year']
    data = all_data['data']
    for year in years:
        for province_id, tmp in data[year].items():
            subject_types = clean_data(str(tmp['type']))
            batches = set(map(lambda x: x['name'], tmp['batch']))
            batches = clean_batch_data(batches)
            for subject_type in subject_types:
                for batch in batches:
                    sql = f"INSERT INTO ProvinceBatch (year, province_id, batch, subject_type) VALUES " \
                          f"('{year}', '{province_id}', '{batch}', '{subject_type}')"
                    c.execute(sql)
                    print(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_province_batch()
