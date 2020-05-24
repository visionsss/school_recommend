from django.shortcuts import render
from . import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def profession(request, search, level_1, level_2):
    def get_recommend_list():
        """获取推荐列表"""
        def cal2(query):
            max_hot = query[0].hot
            min_hot = query[-1].hot
            for i in range(len(query)):
                query[i].hot = (query[i].hot - min_hot) / (max_hot - min_hot)
            query.sort(key=lambda x: x.hot, reverse=True)
            return query
        def cal(query, pre_special: models.Special):
            """计算"""
            max_hot = query[0].hot
            min_hot = query[-1].hot
            for i in range(len(query)):
                query[i].hot = (query[i].hot-min_hot)/(max_hot-min_hot)
                if query[i].level_1 == pre_special.level_1:
                    query[i].hot = query[i].hot + 0.5
                    if query[i].level_2 == pre_special.level_2:
                        query[i].hot = query[i].hot + 0.3
                        if query[i].level_3 == pre_special.level_3:
                            query[i].hot = query[i].hot + 0.2
            query.sort(key=lambda x: x.hot, reverse=True)
            return query
        dic = {'I': ['理学', '工学', '生物与化工大类', '电子信息大类'],
               'A': ['哲学', '文学', '历史学', '艺术学', '文化艺术大类'],
               'S': ['经济学', '法学', '教育学', '医学', '管理学', '资源环境与安全大类',
                     '能源动力与材料大类', '交通运输大类', '医药卫生大类', '新闻传播大类',
                     '教育与体育大类', '公安与司法大类', '公共管理与服务大类'],
               'E': ['管理学'],
               'C': ['管理学', '食品药品与粮食大类', '财经商贸大类', '旅游大类'],
               'R': ['理学', '工学', '农学', '农林牧渔大类', '资源环境与安全大类',
                     '土木建筑大类', '水利大类', '装备制造大类', '轻工纺织大类', '食品药品与粮食大类'],
               }
        res = list(models.Special.objects.order_by('-hot'))
        if request.session.get('username') is None or not models.User.objects.get(username=request.session.get('username')).people_type:
            if request.session.get('pre_special') is None:
               res = cal2(list(res))
            else:
                res = cal(query=list(res), pre_special=models.Special.objects.get(special_id=request.session.get('pre_special')))
        else:
            people_type = models.User.objects.get(username=request.session.get('username')).people_type
            for score, ch in zip([5, 4, 3, 1, 1, 1], people_type):
                for i in range(len(res)):
                    if res[i].level_2 in dic[ch]:
                        res[i].hot = res[i].hot * score
            if request.session.get('pre_special') is None:
                res = cal2(list(res))
            else:
                res = cal(query=list(res), pre_special=models.Special.objects.get(special_id=request.session.get('pre_special')))
        for i in res[:10]:
            i.hot = round(i.hot, 2)
        return res[:10]
    def get_level_2_name_set(search, level_1, level_2):
        level_2_name_list = models.Special.objects.filter(level_1__contains=level_1).order_by('-level_1').distinct()
        level_2_name_set = []
        for i in level_2_name_list:
            if i.level_2 not in level_2_name_set:
                level_2_name_set.append(i.level_2)
        return level_2_name_set
    profession_recommend_list = get_recommend_list()
    search = search[:-1]
    level_1 = level_1[:-1]
    level_2 = level_2[:-1]
    level_2_name_set = get_level_2_name_set(search, level_1, level_2)
    special_data = models.Special.objects.all()
    if search != '':
        special_data = special_data.filter(special_name__contains=search)
    if level_1 != '':
        special_data = special_data.filter(level_1=level_1)
    if level_2 != '':
        special_data = special_data.filter(level_2=level_2)
    special_data = special_data.order_by('pk')
    # 分页
    paginator = Paginator(special_data, 10)  # 设置每一页显示几条  创建一个panginator对象
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
    return render(request, 'Profession/Profession.html', locals())


def profession_detail(request, special_id):
    def get_rank():
        res = [models.Special.objects.filter(level_1=special.level_1, hot__gt=special.hot).count() + 1,
               models.Special.objects.filter(level_1=special.level_1, level_2=special.level_2,
                                             hot__gt=special.hot).count() + 1,
               models.Special.objects.filter(level_1=special.level_1, level_2=special.level_2, level_3=special.level_3,
                                             hot__gt=special.hot).count() + 1]
        return res

    special = models.Special.objects.get(special_id=special_id)
    if special.degree == 'nan':
        special.degree = '无'
    (rank1, rank2, rank3) = get_rank()
    request.session['pre_special'] = special.special_id
    return render(request, 'Profession/Profession_detail.html', locals())
