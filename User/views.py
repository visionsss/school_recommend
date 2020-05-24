from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from . import models
from django.contrib import messages
import json


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if models.User.objects.filter(username=username).exists():
            username_error = '用户已存在'
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')
        if password != re_password:
            re_password_error = '两次密码不一致'
        if not models.User.objects.filter(username=username).exists() and password == re_password:
            user = models.User.objects.create(username=username, password=password)
            return redirect('../login')
    return render(request, 'User/register.html', locals())


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = models.User.objects.filter(username=username)
        if not user.exists():
            username_error = '用户不存在，请先注册'
        if user.exists() and password != user[0].password:
            password_error = '密码错误'
        if user.exists() and password == user[0].password:
            request.session['is_login'] = True
            request.session['username'] = user[0].username
            return redirect('../../')
    return render(request, 'User/login.html', locals())


def logout(request):
    # next_url = request.GET.get('next', '/')
    request.session.flush()
    return redirect('/')


@csrf_exempt
def info(request):
    username = request.session.get('username')
    is_login = request.session.get('is_login')
    if not is_login:
        return redirect('/User/login')
    user = models.User.objects.get(username=username)
    if request.method == 'POST':
        error_flag = False
        n_username = request.POST.get('username')
        n_province_id = request.POST.get('province')
        n_province = models.Province.objects.get(province_id=n_province_id)
        n_subject_type = request.POST.get('subject_type')
        n_score = request.POST.get('score')
        if username != n_username:
            if models.User.objects.filter(username=n_username).exists():
                username_error = '该用户名已存在'
                error_flag = True
        if n_province.province_id in [31, 33]:
            if n_subject_type != '3':
                subject_type_error = '上海、浙江地区请选择综合'
                error_flag = True
        else:
            if n_subject_type == '3':
                subject_type_error = '非上海、浙江地区请选择文科或理科'
                error_flag = True
        if not error_flag:
            user.username = n_username
            user.subject_type = n_subject_type
            user.score = n_score
            user.province = n_province
            models.User.objects.get(username=request.session['username']).delete()
            user.save()
            request.session['username'] = user.username
            success_message = '成功修改'
    return render(request, 'User/info.html', locals())


def index(request):
    return render(request, 'User/index.html', locals())
