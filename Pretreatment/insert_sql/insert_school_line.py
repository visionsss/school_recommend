from glob import glob
import os
from Pretreatment.insert_sql import utils
import re


def get_all_path(path='../result/school_line'):
    all_path = glob(os.path.join(path, '*'))
    return all_path


def insert_school_line():
    conn, c = utils.connect_sql()
    c.execute(f"SELECT province_id FROM Province")
    province_id_list = list(map(lambda x: int(x[0]), c.fetchall()))
    print(province_id_list)
    for path in get_all_path():
        school_id = re.findall('([0-9]{2,5}).csv', path)[0]
        df = utils.read_csv(path, index=True)
        for row in df.itertuples():
            province_id, year, subject_type, score = row[1], row[2], row[3], row[4]
            if province_id not in province_id_list:
                continue
            # print(school_id, province_id, year, types, score)
            sql = f"INSERT INTO SchoolLine (school_id, province_id, year, subject_type, score) VALUES ('{school_id}" \
                  f"', '{province_id}', '{year}', '{subject_type}', '{score}')"
            print(sql)
            c.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_school_line()
