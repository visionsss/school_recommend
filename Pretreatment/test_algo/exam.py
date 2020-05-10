from Pretreatment.test_algo import utils


def get_test():
    """2019年的x:province_id, school_id, subject_type, y是score"""
    conn, c = utils.connect_sql()
    sql = f"SELECT province_id, school_id, subject_type, score FROM SchoolLine WHERE province_id=44 and year=2019"
    c.execute(sql)
    res = c.fetchall()
    x = list(map(lambda xx: xx[:3], res))
    y = list(map(lambda xx: xx[3], res))
    return x, y


def predict(province_id, school_id, subject_type):
    pre_school_line = utils.get_pre_school_line(school_id=school_id, province_id=province_id, subject_type=subject_type)
    province_line = utils.get_province_line(pre_school_line, subject_type=subject_type, province_id=province_id)
    add_x = 0
    for year, score in pre_school_line.items():
        add_x += score-province_line[year]
    add_x = add_x//len(pre_school_line.keys())
    pred = province_line[2019] + add_x
    return pred


def rmse(y, pre_y):
    sum_ = 0
    for i in range(len(y)):
        sum_ += ((y[i]-pre_y[i])**2)
    return (sum_/len(y))**0.5


def mae(y, pre_y):
    sum_ = 0
    for i in range(len(y)):
        sum_ += abs(y[i]-pre_y[i])
    return sum_/len(y)


def get_school_pre_dict(province_id, subject_type):
    conn, c = utils.connect_sql()
    sql = f"SELECT school_id FROM School"
    c.execute(sql)
    res = c.fetchall()
    school_list = list(map(lambda xx: xx[0], res))
    school_pre_dict = {}
    for school_id in school_list:
        school_pre_dict[school_id] = predict(province_id, school_id, subject_type)
    return school_pre_dict


def main():
    x, y = get_test()
    pre_y = [0 for i in range(len(y))]
    for index, (province_id, school_id, subject_type) in enumerate(x):
        pred = predict(province_id, school_id, subject_type)
        pre_y[index] = pred
    print(f'school num: {len(y)}')
    print(f'true school line', y)
    print(f'pred school line', pre_y)
    # rmse_score = rmse(y, pre_y)
    # print(rmse_score)
    mae_score = mae(y, pre_y)
    print(f'mae score:', mae_score)


if __name__ == '__main__':
    main()
