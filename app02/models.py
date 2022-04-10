from django.db import models


# Create your models here.

class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name="部门标题", max_length=32)  # 默认返回对象

    def __str__(self):
        return self.title  # 返回对象里的title


class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)


class User(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2)
    create_date = models.DateTimeField(verbose_name="入职时间")  # ---------->有年月日时分秒
    # create_date = models.DateTimeField(verbose_name="入职时间")---------->只有年月日

    # depart_id = models.BigIntegerField(verbose_name="部门id")   ->这样无约束，ID可能随意的写

    # 有约束
    #  — ForeignKey： 表示设置外键
    #  - to：与哪张表关联
    #  - to_fields： 与表中的哪一列关联，即外键关联的主键
    # 注意：
    # Django自动将写的depart生成depart_id，即数据库表中列名是depart_id，不是depart
    #   级联删除：
    # depart = models.ForeignKey(to="Department", to_fields="id",on_delete=models.CASCADE)
    #   置空：会把外键设置为null，前提是depart列允许为null（下面代码：null=True, blank=True）。
    # 所属部门
    depart = models.ForeignKey(verbose_name="所属部门", to="Department",
                               to_field="id",
                               null=True, blank=True,
                               on_delete=models.SET_NULL)

    # 性别：
    # 在Django中做的约束
    gender_choices = (
        (1, "男1"),
        (2, "女"),

    )
    gender = models.SmallIntegerField(verbose_name="性别",
                                      choices=gender_choices, default=1)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    # null=True, blank=True: 允许为空
    price = models.IntegerField(verbose_name="价格", default=0, null=True, blank=True)

    # 靓号等级,默认情况下为1
    level_choices = (
        (1, '1级'),
        (2, '2级'),
        (3, '3级'),
        (4, '4级')
    )
    level = models.SmallIntegerField(verbose_name='级别',
                                     choices=level_choices, default=1)
    # 靓号状态，默认情况下为2
    status_choices = (
        (1, "已占用"),
        (2, "未使用")
    )
    status = models.SmallIntegerField(verbose_name="状态",
                                      choices=status_choices, default=2)



