from django.db import models


# Create your models here.

class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="部门标题", max_length=32)


class User(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(verbose_name="入职时间")
