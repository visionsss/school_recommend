from django.urls import path
from . import views

urlpatterns = [
    # path('', views.profession),
    path('search=<str:search>level_1=<str:level_1>level_2=<str:level_2>', views.profession),
    path('Profession_detail/<int:special_id>', views.profession_detail),
]
