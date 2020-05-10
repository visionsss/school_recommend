from django.views.decorators.csrf import csrf_exempt    # 取消csrf
from django.shortcuts import render, redirect
from django.db.models import Avg, Max, Min
from . import models
from User.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from Pretreatment.test_algo import utils
import pickle
from .get_recommend_list import get_recommend_list


class SchoolType:
    def __init__(self, school_id, name, score, num_master, num_doctor, level_name, type_name, province_id, city):
        self.school_id = school_id
        self.name = name
        self.score = score
        self.num_master = num_master
        self.num_doctor = num_doctor
        self.level_name = level_name
        self.type_name = type_name
        self.province_id = province_id
        self.city = city
        self.sim = 0

    def __str__(self):
        return self.name + str(self.sim)

    def cal_sim(self, other):
        self.sim += 10/(abs(self.score-other.score)+10) * 50
        self.sim += 1/(abs(self.num_master-other.num_master)+1)*5
        self.sim += 1 / (abs(self.num_doctor - other.num_doctor) + 1) * 5
        if self.level_name == other.level_name:
            self.sim += 5
        if self.type_name == other.type_name:
            self.sim += 5
        if self.province_id == other.province_id:
            self.sim += 25
            if self.city == other.city:
                self.sim += 5


@csrf_exempt
def school_recommend(request):
    if not request.session.get('username'):
        return redirect('/User/login')
    user = User.objects.get(username=request.session.get('username'))
    if request.method == 'POST':
        error_flag = False
        n_province_id = request.POST.get('province')
        n_province = models.Province.objects.get(province_id=n_province_id)
        n_subject_type = request.POST.get('subject_type')
        n_score = request.POST.get('score')
        if n_province.province_id in [31, 33]:
            if n_subject_type != '3':
                subject_type_error = '上海、浙江地区请选择综合'
                error_flag = True
        else:
            if n_subject_type == '3':
                subject_type_error = '非上海、浙江地区请选择文科或理科'
                error_flag = True
        if not error_flag:
            user.subject_type = n_subject_type
            user.score = n_score
            user.province = n_province
            User.objects.get(username=request.session['username']).delete()
            user.save()
            success_message = '成功修改'

    recommend_list = get_recommend_list(user)
    # 分页
    paginator = Paginator(recommend_list, 8)  # 设置每一页显示几条  创建一个panginator对象
    last = paginator.num_pages
    try:
        current_num = int(request.GET.get('page', 1))  # 当你在url内输入的?page = 页码数  显示你输入的页面数目 默认为第1页
        data_list = paginator.page(current_num)
    except EmptyPage:
        current_num = last
        data_list = paginator.page(last)  # 当你输入的page是不存在的时候就会报错

    if paginator.num_pages > 11:  # 如果分页的数目大于11
        if current_num - 5 < 1:  # 你输入的值
            page_range = range(1, 11)  # 按钮数
        elif current_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
            page_range = range(current_num - 5, current_num + 1)  # 显示的按钮数

        else:
            page_range = range(current_num - 5, current_num + 6)  # range求的是按钮数   如果你的按钮数小于分页数 那么就按照正常的分页数目来显示

    else:
        page_range = range(1, last)  # 正常分配
    return render(request, 'School/School_recommend.html', locals())


@csrf_exempt
def school_detail(request, school_id):
    def get_sim_school(school_class):
        pkl_file = f'./static/sim_school/{school_class.pk}.json'
        if os.path.exists(pkl_file):
            with open(pkl_file, 'rb') as f:
                res = pickle.load(f)
            for i in res[1:11]:
                i.sim = round(i.sim)
            return res[1: 11]
        res = []
        for i in models.School.objects.all():
            score = models.SchoolLine.objects.filter(school_id=i.school_id).aggregate(Avg('score'))['score__avg']
            if score is None:
                score = 500
            res.append(SchoolType(i.school_id, i.name, score, i.num_master, i.num_doctor, i.level_name, i.type_name, i.province.province_id, i.city))
        score = models.SchoolLine.objects.filter(school_id=school_class.school_id).aggregate(Avg('score'))['score__avg']
        if score is None:
            score = 500
        other = SchoolType(school_class.school_id, school_class.name, score, school_class.num_master, school_class.num_doctor, school_class.level_name, school_class.type_name, school_class.province.province_id, school_class.city)
        for i in res:
            i.cal_sim(other)
        res = sorted(res, key=lambda x: x.sim, reverse=True)
        with open(pkl_file, 'wb') as f:
            pickle.dump(res, f)
        for i in res[1:11]:
            i.sim = round(i.sim)
        return res[1: 11]
    if models.School.objects.filter(school_id=school_id).count() == 0:
        school_detail_error = '没有此院校'
    else:
        school_class = models.School.objects.get(school_id=school_id)
        sim_school_list = get_sim_school(school_class)
        school_line = models.SchoolLine.objects.filter(school_id=school_id).order_by('-province', '-year')
        if request.method == 'POST':
            search = request.POST.get('search')
            school_line = school_line.filter(province__province_name__contains=search)
    return render(request, 'School/School_detail.html', locals())


@csrf_exempt
def school(request, search, province_id):
    province_list = models.Province.objects.all()
    school_list = models.School.objects.all()
    search = search[:-1]
    school_list = school_list.filter(name__contains=search)
    if province_id != '&':
        province_id = int(province_id[:-1])
        school_list = school_list.filter(province=province_id)

    # 分页
    paginator = Paginator(school_list, 8)  # 设置每一页显示几条  创建一个panginator对象
    last = paginator.num_pages
    try:
        current_num = int(request.GET.get('page', 1))  # 当你在url内输入的?page = 页码数  显示你输入的页面数目 默认为第1页
        data_list = paginator.page(current_num)
    except EmptyPage:
        current_num = last
        data_list = paginator.page(last)  # 当你输入的page是不存在的时候就会报错

    if paginator.num_pages > 11:  # 如果分页的数目大于11
        if current_num - 5 < 1:  # 你输入的值
            page_range = range(1, 11)  # 按钮数
        elif current_num + 5 > paginator.num_pages:  # 按钮数加5大于分页数
            page_range = range(current_num - 5, current_num + 1)  # 显示的按钮数

        else:
            page_range = range(current_num - 5, current_num + 6)  # range求的是按钮数   如果你的按钮数小于分页数 那么就按照正常的分页数目来显示

    else:
        page_range = range(1, last)  # 正常分配
    return render(request, 'School/School.html', locals())