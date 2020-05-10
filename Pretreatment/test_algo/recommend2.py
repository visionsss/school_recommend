"""假装运行django"""
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school_recommend.settings")
django.setup()
from typing import List

from Pretreatment.test_algo import utils, exam
import matplotlib.pyplot as plt
import math
import sqlite3
import pickle


class SchoolRecommend:
    def __init__(self, province_id: int, recommend_score, predict_score):
        self.province_id = province_id
        self.recommend_score = recommend_score
        self.predict_score = predict_score

    def __str__(self):
        return str(self.predict_score)


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


def get_pkl(score, subject_type, province_id):
    file = rf"E:\pycharm_project\school_recommend\static\recommend_school\province_id{province_id}subject_type{subject_type}score{score}"
    res = []
    with open(file, 'rb') as f:
        s = pickle.load(f)
    for i in s:
        res.append(i.school_class.school_id)
    return res


def main():
    province_id = utils.province_name_to_province_id('河南')[0]
    df1, df2 = utils.div_read_test()
    with open('../../static/school_pre_dic.json', 'rb') as f:
        school_pre_dic = pickle.load(f)

    y = []
    pre_y = []
    for row in df1.itertuples():
        index, score, school_name, subject_type = row
        y.append(school_name)
        pre_y.append(get_pkl(score, subject_type, province_id))
    for i in range(len(y)):
        y[i] = utils.school_name_to_school_id(y[i])[0]
    plt_x1 = []
    plt_y1 = []
    for k in range(0, 2006, 5):
        score = hit_score(k, y, pre_y)
        plt_x1.append(k)
        plt_y1.append(score)
    y = []
    pre_y = []
    for row in df2.itertuples():
        index, score, school_name, subject_type = row
        y.append(school_name)
        pre_y.append(get_pkl(score, subject_type, province_id))
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
