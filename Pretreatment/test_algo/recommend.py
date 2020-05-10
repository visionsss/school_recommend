from Pretreatment.test_algo import utils, exam
import matplotlib.pyplot as plt
import math


def predict(province_id, school_id, subject_type):
    pre_school_line = utils.get_pre_school_line(school_id=school_id, province_id=province_id, subject_type=subject_type)
    province_line = utils.get_province_line(pre_school_line, subject_type=subject_type, province_id=province_id)
    add_x = 0
    for year, score in pre_school_line.items():
        add_x += score-province_line[year]
    add_x = add_x//len(pre_school_line.keys())
    pred = province_line[2019] + add_x
    return pred


def recommend(score: int, subject_type: int, province_id: int, school_pre_dict: dict) -> list:
    res = {}
    for school_id, score_ in school_pre_dict.items():
        res[school_id] = 1/(abs(score-score_+20)/100+1)
    school_id_list = utils.get_school_province(province_id)  # 获取与该同学相同省份的院校
    for school_id in school_id_list:
        res[school_id] = res[school_id] * 8
    rr = sorted(res.items(), key=lambda x: x[1], reverse=True)
    school_list = list(map(lambda x: x[0], rr))
    return school_list


def hit_score(k, y, pre_y):
    hit = 0
    for i, school_name in enumerate(y):
        if school_name in pre_y[i][:k]:
            hit += 1

    return hit/len(y)


def draw(x1, y1, x2, y2, label):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title(label)
    plt.xlabel('推荐院校数目n(个)', fontdict={'weight': 'normal', 'size': 15})
    plt.ylabel('命中率hit rate(%)', fontdict={'weight': 'normal', 'size': 15})
    plt.plot(x1, y1, marker='*')
    plt.plot(x2, y2, marker='o')
    plt.legend(['理科', '文科'])
    plt.show()


def main():
    province_id = utils.province_name_to_province_id('河南')[0]
    df1, df2 = utils.div_read_test()
    school_pre_dict1 = exam.get_school_pre_dict(province_id, '1')
    y = []
    pre_y = []
    for row in df1.itertuples():
        index, score, school_name, subject_type = row
        y.append(school_name)
        pre_y.append(recommend(score, subject_type, province_id, school_pre_dict1))
    for i in range(len(y)):
        y[i] = utils.school_name_to_school_id(y[i])[0]
    plt_x1 = []
    plt_y1 = []
    for k in range(0, 50, 5):
        score = hit_score(k, y, pre_y)
        plt_x1.append(k)
        plt_y1.append(score)
    school_pre_dict2 = exam.get_school_pre_dict(province_id, '2')
    y = []
    pre_y = []
    for row in df1.itertuples():
        index, score, school_name, subject_type = row
        y.append(school_name)
        pre_y.append(recommend(score, subject_type, province_id, school_pre_dict2))
    for i in range(len(y)):
        y[i] = utils.school_name_to_school_id(y[i])[0]
    plt_x2 = []
    plt_y2 = []
    for k in range(0, 50, 5):
        score = hit_score(k, y, pre_y)
        plt_x2.append(k)
        plt_y2.append(score)
    draw(plt_x1, plt_y1, plt_x2, plt_y2, '命中率曲线图')


if __name__ == '__main__':
    main()
