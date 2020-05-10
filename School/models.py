from django.db import models


class Province(models.Model):
    """省份表"""
    province_id = models.IntegerField(primary_key=True, help_text='省份id')
    province_name = models.CharField(max_length=20, help_text='省份名称')

    class Meta:
        db_table = 'Province'
        ordering = ['province_id']
        verbose_name = '省份'
        verbose_name_plural = '省份'

    def __str__(self):
        return self.province_name


class School(models.Model):
    """院校信息表"""
    school_id = models.IntegerField(primary_key=True, help_text='院校id')
    name = models.CharField(max_length=128, help_text='院校名称')
    level_name = models.CharField(max_length=128, help_text='层次')
    type_name = models.CharField(max_length=128, help_text='类别')
    belong = models.CharField(max_length=128, help_text='隶属部门')
    f985 = models.IntegerField(help_text='985')
    f211 = models.IntegerField(help_text='211')
    province = models.ForeignKey('Province', on_delete=models.CASCADE)
    city = models.CharField(max_length=128, help_text='城市')
    county = models.CharField(max_length=128, help_text='地区')
    nature_name = models.CharField(max_length=128, help_text='公办或民办')
    dual_class_name = models.CharField(max_length=128, help_text='双一流')
    hot = models.IntegerField(help_text='热度')
    logo = models.CharField(max_length=256, help_text='校徽')
    num_subject = models.IntegerField(help_text='重点学科')
    num_master = models.IntegerField(help_text='硕士点')
    num_doctor = models.IntegerField(help_text='博士点')
    short = models.CharField(max_length=256, help_text='简称')
    rank = models.CharField(max_length=256, help_text='排名')
    email = models.CharField(max_length=256, help_text='邮箱')
    address = models.CharField(max_length=256, help_text='地址')
    phone = models.CharField(max_length=256, help_text='电话')
    site = models.CharField(max_length=256, help_text='网站')
    create_date = models.CharField(max_length=256, help_text='建校日期例如1990')
    area = models.CharField(max_length=256, help_text='地区')

    class Meta:
        db_table = 'School'
        ordering = ['school_id']
        verbose_name = '院校信息'
        verbose_name_plural = '院校信息'

    def __str__(self):
        return self.name


class ProvinceLine(models.Model):
    province = models.ForeignKey('Province', help_text='省份id', on_delete=models.CASCADE)
    year = models.IntegerField(help_text='年份')
    subject_type = models.CharField(max_length=128, help_text='类别')
    batch = models.CharField(max_length=128, help_text='批次')
    score = models.IntegerField(help_text='分数')

    class Meta:
        db_table = 'ProvinceLine'
        ordering = ['province_id', 'year']
        verbose_name = '省分数线'
        verbose_name_plural = '省分数线'

    def __str__(self):
        return str(self.province) + str(self.year) + self.batch


class SchoolLine(models.Model):
    school = models.ForeignKey('School', help_text='院校id', on_delete=models.CASCADE)
    province = models.ForeignKey('Province', help_text='省份id', on_delete=models.CASCADE)
    year = models.IntegerField(help_text='年份')
    subject_type = models.CharField(max_length=128, help_text='类别')
    score = models.IntegerField(help_text='分数')

    class Meta:
        db_table = 'SchoolLine'
        ordering = ['school_id', 'province_id']
        verbose_name = '院校分数线'
        verbose_name_plural = '院校分数线'

    def __str__(self):
        return str(self.school) + str(self.province) + str(self.year)


class ProvinceBatch(models.Model):
    year = models.IntegerField(help_text='年份')
    province = models.ForeignKey('Province', help_text='省份id', on_delete=models.CASCADE)
    subject_type = models.CharField(max_length=128, help_text='类别')
    batch = models.CharField(max_length=128, help_text='批次')
    score = models.IntegerField(help_text='分数线', default=0)

    class Meta:
        db_table = 'ProvinceBatch'
        ordering = ['year', 'province_id']
        verbose_name = '省份批次'
        verbose_name_plural = '省份批次'

    def __str__(self):
        return str(self.batch) + str(self.province) + str(self.year)
