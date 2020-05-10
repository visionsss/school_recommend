import sqlite3
import pickle


def connect_sql(path='../db.sqlite3') -> (sqlite3.connect, sqlite3.Cursor):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    return conn, c


def get_pre_school_line(school_id: int, subject_type: int, province_id: int) -> dict:
    """获取之前年份的院校分数线"""

    def get_other_province_school_line() -> int:
        """找不到之前的院校分数线，就其他省份取平均，还找不到直接返回450"""
        sql_ = f"SELECT AVG(score) FROM SchoolLine WHERE year=2018 and school_id='{school_id}' " \
               f"and subject_type='{subject_type}'"
        c.execute(sql_)
        score = c.fetchone()
        if not score[0]:
            return 450
        return int(score[0])

    res = dict()
    sql = f"SELECT year, score FROM SchoolLine WHERE school_id='{school_id}' and subject_type='{subject_type}' and" \
          f" province_id='{province_id}' and year==2018"
    c.execute(sql)
    all_data = c.fetchall()
    if not all_data:
        return {2018: get_other_province_school_line()}
    for row in all_data:
        res[row[0]] = row[1]
    return res


def get_province_line(pre_school_line: dict, subject_type: int, province_id: int) -> dict:
    """获取省分数线"""
    def select_batch():
        """获取最合适的batch"""
        # 得到候选批次
        sql_ = f"SELECT DISTINCT batch FROM ProvinceBatch WHERE year=2019 and subject_type={subject_type}" \
               f" and province_id={province_id}"
        c.execute(sql_)
        batches = list(map(lambda x: x[0], c.fetchall()))
        # 查找最适合的批次
        for year, score in pre_school_line.items():
            sql_ = f"SELECT * FROM ProvinceBatch WHERE year={year} and subject_type={subject_type}" \
                   f" and province_id={province_id}"
            c.execute(sql_)
            res = c.fetchall()
            res = sorted(res, key=lambda x: x[5], reverse=True)
            # print(res)
            for row in res:
                # print(row, score, batches)
                if row[5] <= score and row[3] in batches:
                    return row[3]

    batch = select_batch()
    # print(batch, pre_school_line)
    res_dict = {}
    years = list(pre_school_line.keys())
    years.append(2019)
    for year in years:
        sql = f"SELECT * FROM ProvinceBatch WHERE year={year} and subject_type={subject_type}" \
               f" and province_id={province_id} and batch='{batch}'"
        c.execute(sql)
        res = c.fetchone()
        if res:
            res_dict[year] = res[4]
        else:
            res_dict[year] = 450
    return res_dict


def get_predict_score(province_id, school_id, subject_type):

    pre_school_line = get_pre_school_line(school_id=school_id, province_id=province_id, subject_type=subject_type)
    return pre_school_line[2018]

    # province_line = get_province_line(pre_school_line, subject_type=subject_type, province_id=province_id)
    # add_x = 0
    # for year, score in pre_school_line.items():
    #     add_x += score - province_line[year]
    # add_x = add_x // len(pre_school_line.keys())
    # pred = province_line[2019] + add_x
    # return pred


def main():
    dic = {}
    c.execute(f"SELECT province_id FROM Province")
    province_list = list(map(lambda x: x[0], c.fetchall()))
    c.execute(f"SELECT school_id FROM School")
    school_list = list(map(lambda x: x[0], c.fetchall()))
    for province_id in province_list:
        dic[province_id] = {}
        subject_list = [1, 2]
        if province_id in [31, 33]:
            subject_list = [3]
        for school_id in school_list:
            dic[province_id][school_id] = {}
            for subject_type in subject_list:
                print(province_id, school_id, subject_type, end=' ')
                dic[province_id][school_id][subject_type] = get_predict_score(province_id, school_id, subject_type)
                print(dic[province_id][school_id][subject_type])
                # break
            # break
        # break

    with open('../static/school_pre_dic.json', 'wb') as f:
        pickle.dump(dic, f)
    print(dic)


if __name__ == '__main__':
    conn, c = connect_sql()
    main()
