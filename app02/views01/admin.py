# -*- coding:utf-8 -*-
"""
----------------------------------------------------------
作者: 武广辉
日期: 2022/4/4 10:44
----------------------------------------------------------
当前项目的名称:                    管理员管理
在文件创建过程中在“新建文件”对话框中指定的新文件的名称: admin.py
当前集成开发环境: PyCharm
----------------------------------------------------------
"""
from django import forms
from django.shortcuts import render

from app02 import models
from app02.utils.pagination import Pagination
from django.shortcuts import render, redirect
from app02.utils.pagination import Pagination
from app02 import models

def admin_list(request):
    """管理员列表"""

    ### 查找
    data_dict = {}  # 设一个空字典
    value = request.GET.get("res1", "")
    if value:  # 用户通过url传入关键字，只有输入了关键字不为空了，才往字典里写入这个值
        # data_dict = {"username__contains": value}
        data_dict['username__contains'] = value
    # 根据关键字，去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    page_object = Pagination(request, queryset, page_size=3)
    context = {
        'queryset1': page_object.page_queryset,     # 分完页的数据
        'page_string': page_object.html(),          # 生成的页码
        'value1': value
    }
    return render(request, "admin_list.html", context)


class AdminModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput()   # 设为密码输入框，可以隐藏密码
        }


def admin_add(request):
    """管理员添加"""
    if request.method == "GET":

        form = AdminModelForm()
        return render(request, 'admin_modelform_add.html', {"form1": form})
    else:
        form = AdminModelForm(data=request.POST)   # 接收用户输入的值
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")
        return render(request, "admin_modelform_add.html", {"form1": form})  # 通过render将对象传入到HTML中。


def admin_edit(request):
    """编辑管理员"""
    if request.method == "GET":
        nid2 = request.GET.get("nid1")
        # 根据id先获取这个id所对应的那一行的数据（对象）（name，password等）
        row_object = models.Admin.objects.filter(id=nid2).first()
        # 在AdminModelform里加了instance，ModelForm默认会把数据加在输入框里
        form = AdminModelForm(instance=row_object)
        return render(request, "admin_edit.html", {'form': form})

    nid2 = request.GET.get("nid1")
    row_object = models.Admin.objects.filter(id=nid2).first()
    # POST方式提交（用户输入信息后提交），然后进行数据校验（默认不允许为空）。
    # instance=row_object：保证后面的form.save更新到当前数据，而不是新添加一行数据
    form: AdminModelForm = AdminModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()  # modelform里的方法：自动将用户提交的数据存储到表（User）里
        return redirect('/admin/list/')
    return render(request, 'admin_list.html', {'form': form})


def admin_delete(request):
    """用户删除"""

    nid2 = request.GET.get("nid1")
    row_object = models.Admin.objects.filter(id=nid2).delete()
    return redirect("/admin/list/")
