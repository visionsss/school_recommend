import pandas as pd
import sqlite3


def connect_sql(path='../../db.sqlite3') -> (sqlite3.connect, sqlite3.Cursor):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    return conn, c


def read_test_data(subject_type='l') -> pd.DataFrame:
    """
    subject_type='l' or subject_type='w'
    """
    path = f'../test_algo/test_data/fsk_{subject_type}_0305.xls'
    df = pd.read_excel(path)
    df = df.iloc[:, 1:]
    df.dropna(axis=0, how='any', inplace=True)
    del_index = []
    for row in df.itertuples():
        index, score, school_name = row
        school_name = school_name.split('(')[0]
        df.loc[index, 'yxmc'] = school_name
        if not school_name_to_school_id(school_name):
            del_index.append(index)
            print(school_name)
            print(del_index)
    df.drop(index=del_index, axis=0, inplace=True)
    if subject_type == 'l':
        df['subject_type'] = 1
    else:
        df['subject_type'] = 2

    df.columns = ['score', 'school_name', 'subject_type']
    return df


def province_name_to_province_id(province_name):
    conn, c = connect_sql()
    sql = f"SELECT province_id FROM Province WHERE province_name='{province_name}'"
    # print(sql)
    c.execute(sql)
    return c.fetchone()


def province_id_to_province_name(province_id):
    conn, c = connect_sql()
    sql = f"SELECT province_name FROM Province WHERE province_id='{province_id}'"
    # print(sql)
    c.execute(sql)
    return c.fetchone()


def school_name_to_school_id(school_name):
    conn, c = connect_sql()
    sql = f"SELECT school_id FROM School WHERE name='{school_name}'"
    # print(sql)
    c.execute(sql)
    return c.fetchone()


def school_id_to_school_name(school_id):
    conn, c = connect_sql()
    sql = f"SELECT name FROM School WHERE school_id='{school_id}'"
    # print(sql)
    c.execute(sql)
    return c.fetchone()


def save_test():
    df1 = read_test_data(subject_type='w')
    df2 = read_test_data(subject_type='l')
    df = pd.concat([df1, df2])
    df.to_csv('./test_data/test.csv')
    return df


def read_test() -> pd.DataFrame:
    # df = pd.read_csv('./test_data/test.csv')
    df = pd.read_csv(r'E:\pycharm_project\school_recommend\Pretreatment\test_algo\test_data\test.csv')
    return df.iloc[:, 1:]


def div_read_test() -> (pd.DataFrame, pd.DataFrame):
    df = read_test()
    df1 = df[df['subject_type'] == 1]
    df2 = df[df['subject_type'] == 2]
    return df1, df2


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
    conn, c = connect_sql()
    sql = f"SELECT year, score FROM SchoolLine WHERE school_id='{school_id}' and subject_type='{subject_type}' and" \
          f" province_id='{province_id}' and year!=2019"
    c.execute(sql)
    all_data = c.fetchall()
    if not all_data:
        return {2018: get_other_province_school_line()}
    for row in all_data:
        res[row[0]] = row[1]
    return res


def get_province_line(pre_school_line: dict, subject_type: int, province_id: int) -> dict:
    conn, c = connect_sql()

    def select_batch():
        """获取最合适的batch"""
        # 得到候选批次
        sql_ = f"SELECT DISTINCT batch FROM ProvinceLine WHERE year=2019 and subject_type={subject_type}" \
               f" and province_id={province_id}"
        c.execute(sql_)
        batches = list(map(lambda x: x[0], c.fetchall()))
        # 查找最适合的批次
        for year, score in pre_school_line.items():
            sql_ = f"SELECT * FROM ProvinceLine WHERE year={year} and subject_type={subject_type}" \
                   f" and province_id={province_id}"
            c.execute(sql_)
            res = c.fetchall()
            res = sorted(res, key=lambda x: x[4], reverse=True)
            for row in res:
                if row[4] <= score and row[3] in batches:
                    return row[3]

    batch = select_batch()
    # print(batch)
    res_dict = {}
    years = list(pre_school_line.keys())
    years.append(2019)
    for year in years:
        sql = f"SELECT * FROM ProvinceLine WHERE year={year} and subject_type={subject_type}" \
               f" and province_id={province_id} and batch='{batch}'"
        c.execute(sql)
        res = c.fetchone()
        if res:
            res_dict[year] = res[4]
        else:
            res_dict[year] = 450
    return res_dict


def get_school_province(province_id):
    conn, c = connect_sql()
    sql = f"SELECT school_id FROM School WHERE province_id={province_id}"
    c.execute(sql)
    res = c.fetchall()
    res = list(map(lambda x: x[0], res))
    return res


def main():
    save_test()


if __name__ == '__main__':
    main()
