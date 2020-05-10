from django.urls import path
from . import views

urlpatterns = [
    path('School_detail/<int:school_id>', views.school_detail, name='院校详细信息'),
    path('recommend/', views.school_recommend, name='院校推荐'),
    path('search=<str:search>province_id=<str:province_id>', views.school, name='院校信息')
]