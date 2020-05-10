from Pretreatment.insert_sql import utils


def insert_province_line():
    # 获取省份id 省份name
    not_in_list = ['艺术', '体育', '自主', '民族', '运动员', '农村', '国家']
    province = set()
    school = utils.read_csv(path='../result/school.csv')
    for province_id, province_name in zip(school['province_id'], school['province_name']):
        province.add((province_id, province_name))
    d = {}
    for k in province:
        d[k[1]] = k[0]

    conn, c = utils.connect_sql()
    data = utils.read_csv(path='../result/province_line.csv')
    for row in data.itertuples():
        province_id = d[row[2]]
        year = row[3].replace('年', '')
        subject_type = row[4]
        if subject_type == '理科':
            subject_type = 1
        elif subject_type == '文科':
            subject_type = 2
        elif subject_type == '综合':
            subject_type=3
        else:
            continue
        batch = row[5]
        flag = True
        for kkk in not_in_list:
            if kkk in batch:
                flag = False
                break
        if not flag:
            continue
        score = row[6]
        sql = f"INSERT INTO ProvinceLine (province_id,year,subject_type,batch,score) VALUES ('{province_id}'," \
              f"'{year}','{subject_type}','{batch}','{score}')"
        print(sql)
        c.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_province_line()
