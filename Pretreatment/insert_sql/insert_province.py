"""
先再school_info/models.py中创建数据库表
1. python manage.py startapp School_   # setting中设置好
2. python manage.py makemigrations
3. python manage.py migrate
"""
from Pretreatment.insert_sql import utils


def insert_province():
    conn, c = utils.connect_sql()
    # 获取省份id 省份name
    province = set()
    school = utils.read_csv(path='../result/school.csv')
    for province_id, province_name in zip(school['province_id'], school['province_name']):
        province.add((province_id, province_name))

    for ids, name in province:
        sql = f"INSERT INTO province (province_id, province_name) VALUES ('{ids}', '{name}')"
        print(sql)
        c.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_province()
