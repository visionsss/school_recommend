from Pretreatment.insert_sql import utils


def insert_special():
    df = utils.read_csv('../result/special.csv', index=True)
    conn, c = utils.connect_sql()
    for row in df.itertuples():
        special_id = row[3]
        level_1 = row[16]
        level_2 = row[2]
        level_3 = row[8]
        special_name = row[9]
        hot = row[7]
        limit_year = row[1]
        degree = row[4]
        print(special_id, level_1, level_2, level_3, special_name, hot, limit_year, degree)
        sql = f"INSERT INTO Special (special_id, level_1, level_2, level_3, special_name, hot, limit_year, degree) " \
              f"VALUES ('{special_id}', '{level_1}', '{level_2}', '{level_3}', '{special_name}', '{hot}', '{limit_year}', '{degree}')"
        print(sql)
        c.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_special()
