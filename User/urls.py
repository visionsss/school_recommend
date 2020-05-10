from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='注册'),
    path('login/', views.login, name='登录'),
    path('info/', views.info, name='信息'),
    path('logout/', views.logout, name='退出')
]
