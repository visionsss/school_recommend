from typing import List
from School import models
from User.models import User
import os
import pickle
import sqlite3


class SchoolRecommend:
    def __init__(self, school_class: models.School, recommend_score, predict_score):
        self.school_class = school_class
        self.recommend_score = recommend_score
        self.predict_score = predict_score

    def __str__(self):
        return self.school_class


def cal(res, province_id: int, score: int) -> List[SchoolRecommend]:
    for i in range(len(res)):
        # print(score, res[i].predict_score)
        res[i].recommend_score = 1 / (abs(int(score) - int(res[i].predict_score) + 20) / 100 + 1)
        if res[i].school_class.province.province_id == province_id:
            res[i].recommend_score *= 1.5
        res[i].recommend_score = round(res[i].recommend_score, 2)

    res = sorted(res, key=lambda x: x.recommend_score, reverse=True)
    return res


def get_recommend_list(user: User) -> List[SchoolRecommend]:
    file = f'./static/recommend_school/province_id{user.province.province_id}subject_type{user.subject_type}score{user.score}'
    with open('./static/school_pre_dic.json', 'rb') as f:
        school_pre_dic = pickle.load(f)
    # print(school_pre_dic[11][30][1])
    if os.path.exists(file):
        with open(file, 'rb') as f:
            res = pickle.load(f)
    else:
        res = []
        school_list = models.School.objects.all()
        for i in school_list:
            try:
                score = school_pre_dic[int(user.province.province_id)][int(i.school_id)][int(user.subject_type)]
            except:
                score = 460
            res.append(SchoolRecommend(i, 0, score))
        res = cal(res, user.province.province_id, user.score)
        with open(file, 'wb') as f:
            pickle.dump(res, f)
    return res
