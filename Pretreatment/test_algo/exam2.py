from Pretreatment.test_algo import utils
import pickle


def get_test():
    """2019年的x:province_id, school_id, subject_type, y是score"""
    conn, c = utils.connect_sql()
    sql = f"SELECT province_id, school_id, subject_type, score FROM SchoolLine WHERE province_id=44 and year=2019"
    c.execute(sql)
    res = c.fetchall()
    x = list(map(lambda xx: xx[:3], res))
    y = list(map(lambda xx: xx[3], res))
    return x, y


def mae(y, pre_y):
    sum_ = 0
    for i in range(len(y)):
        sum_ += abs(y[i]-pre_y[i])
    return sum_/len(y)


def main():
    with open('../../static/school_pre_dic.json', 'rb') as f:
        school_pre_dic = pickle.load(f)
    x, y = get_test()
    pre_y = [0 for i in range(len(y))]
    for index, (province_id, school_id, subject_type) in enumerate(x):
        try:
            pred = school_pre_dic[int(province_id)][int(school_id)][int(subject_type)]
        except:
            pred = 460
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
