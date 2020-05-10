from django.db import models
from User.models import User


class Special(models.Model):
    special_id = models.IntegerField(primary_key=True)
    level_1 = models.CharField(max_length=64, help_text='分类1')
    level_2 = models.CharField(max_length=64, help_text='分类2')
    level_3 = models.CharField(max_length=64, help_text='分类3')
    special_name = models.CharField(max_length=256, help_text='专业名称')
    hot = models.IntegerField(help_text='专业热度')
    limit_year = models.CharField(max_length=256, help_text='所学年份')
    degree = models.CharField(max_length=256, help_text='授予学位名称')

    class Meta:
        db_table = 'Special'
        ordering = ['level_1', 'level_2', 'level_3', 'hot']
        verbose_name = '专业信息'
        verbose_name_plural = '专业信息'

    def __str__(self):
        return self.special_name
