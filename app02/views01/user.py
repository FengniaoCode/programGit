# -*- coding:utf-8 -*-
"""
----------------------------------------------------------
作者: 武广辉
日期: 2022/4/2 18:00
----------------------------------------------------------
当前项目的名称:                    用户管理
在文件创建过程中在“新建文件”对话框中指定的新文件的名称: user.py
当前集成开发环境: PyCharm
----------------------------------------------------------
"""

from django.shortcuts import render, redirect
from app02.utils.pagination import Pagination
from app02 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

"""用户管理"""


def user_list(request):
    # 获取所有用户列表,得到一个个对象[object,object,object]
    queryset = models.User.objects.all()
    # 循环queryset,取出数据库里的id，name，password等值

    """用Python的语法获取数据的方法:"""
    for obj in queryset:
        # obj.create_date是datetime数据类型，所以要转换成字符串类型,只显示年月日【.strftime("%Y-%m-%d")】
        # Django中用choices+元组套元组时，取文本值时用get_gender_display()

        print(obj.id, obj.name, obj.account, obj.create_date.strftime("%Y-%m-%d"), obj.get_gender_display(),
              obj.depart_id, obj.depart.title)
        # obj.depart_id      ————————>获取数据库中那个字段的部门id。然后再根据id查询title值
        id_name = obj.depart_id
        depart_name = models.Department.objects.filter(id=id_name).first()
        print(depart_name.title)
        # 以上这个方法比较繁琐，Django有专门跨表取数据的方法：
        # obj.depart    ————————>根据id自动关联的表中去获取那一行数据，即depart表的对象
        # 区别：obj.depart_id是获取员工表中所存储的部门id值
        #      obj.depart是根据外键关系，获取员工表中部门id自动关联的表（depart表）中的那一行数据（title值）
        print(obj.depart.title)

    """使用分页组件进行分页"""
    page_object = Pagination(request, queryset, page_size=3)  # queryset是数据库查询的总数据，page_size是每页显示的数据的条数
    context = {
        "queryset1": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成的页码
    }

    # 把分完页的数据传到前端页面
    return render(request, "user_list.html", context)


"""添加用户（原始方式）"""


def user_add(request):
    if request.method == "GET":

        context = {
            'gender_choices': models.User.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)

    else:
        # 获取用户提交的数据
        user_name = request.POST.get("name")
        user_pwd = request.POST.get("pwd")
        user_age = request.POST.get("age")
        user_account = request.POST.get("account")
        user_dtime = request.POST.get("dtime")
        user_gd_id = request.POST.get("gd")
        user_depart_id = request.POST.get("depart")

        # 添加到数据库中
        models.User.objects.create(name=user_name, password=user_pwd,
                                   age=user_age, account=user_account,
                                   create_date=user_dtime,
                                   gender=user_gd_id,
                                   depart_id=user_depart_id, )
        # 重定向到用户列表页面
        return redirect("/user/list/")


from django import forms


class UserModelForm(forms.ModelForm):
    # 把那张表转化成form组件
    class Meta:
        # 这个意思即是把User转化成form组件
        model = models.User
        fields = ['name', 'password', 'age', "account", "create_date", "gender", "depart"]
        # 使用插件定义属性
        widgets = {
            # 生成input标签,然后自己定义一个class=form-control（<input type="text" class="form-control">）
            "name": forms.TextInput(attrs={"class": "form-control"}),
            # 生成input标签,然后自己定义一个class=form-control（<input type="password" class="form-control">）
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "age": forms.TextInput(attrs={"class": "form-control"}),
            "account": forms.TextInput(attrs={"class": "form-control"}),
            "create_date": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "depart": forms.Select(attrs={"class": "form-control"})

        }


"""基于ModelForm形式添加用户"""


def user_modelform_add(request):
    # GET方式提交
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "user_modelform_add.html", {"form": form})

    # POST方式提交（用户输入信息后提交），然后进行数据校验（默认不允许为空）
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # 提交后得到的数据：{'name': '枫鸟', 'password': '111', 'age': 22, 'account': Decimal('1122.22'),
        # 'create_date':datetime.datetime(2022, 1, 1, 0, 0, tzinfo=<UTC>),
        # 'gender': 2, 'depart': <Department: 保安科>}
        print(form.cleaned_data)
        form.save()  # modelform里的方法：自动将用户提交的数据存储到表（User）里
        return redirect("/user/list/")

    else:
        # 校验失败（在页面上显示错误信息）
        print(form.errors)
        return render(request, "user_modelform_add.html", {"form": form})


def user_edit(request):
    """编辑用户"""
    if request.method == "GET":
        nid2 = request.GET.get("nid1")
        # 根据id先获取这个id所对应的那一行的数据（对象）（name，password，age，data等）
        row_object = models.User.objects.filter(id=nid2).first()
        # 在Usermodelform里加了instance，ModelForm默认会把数据加在输入框里
        form = UserModelForm(instance=row_object)
        return render(request, "user_edit.html", {'form': form})

    nid2 = request.GET.get("nid1")
    row_object = models.User.objects.filter(id=nid2).first()
    # POST方式提交（用户输入信息后提交），然后进行数据校验（默认不允许为空）。
    # instance=row_object：保证后面的form.save更新到当前数据，而不是新添加一行数据
    form: UserModelForm = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()  # modelform里的方法：自动将用户提交的数据存储到表（User）里
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request):
    """用户删除"""

    nid2 = request.GET.get("nid1")
    row_object = models.User.objects.filter(id=nid2).delete()
    return redirect("/user/list/")
