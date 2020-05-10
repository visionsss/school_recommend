from django.db import models
from School.models import Province, ProvinceBatch


class User(models.Model):
    username = models.CharField(primary_key=True, help_text='用户名', max_length=128)
    password = models.CharField(max_length=128, help_text='密码', blank=True)
    province = models.ForeignKey('School.Province', on_delete=models.CASCADE, default=44, help_text='省份/外键')
    subject_type = models.CharField(max_length=128, default='1', help_text='类别')
    score = models.IntegerField(help_text='高考分数', default=500)
    people_type = models.CharField(max_length=128)

    class Meta:
        db_table = 'User'
        ordering = ['username']
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.username
