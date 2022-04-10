# -*- coding:utf-8 -*-
"""
----------------------------------------------------------
作者: 武广辉
日期: 2022/4/2 18:01
----------------------------------------------------------
当前项目的名称:                    靓号管理
在文件创建过程中在“新建文件”对话框中指定的新文件的名称: pretty.py
当前集成开发环境: PyCharm
----------------------------------------------------------
"""
from django import forms
from django.utils.safestring import mark_safe
from django.shortcuts import render, redirect
from app02.utils.pagination import Pagination
from app02 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

"""靓号管理"""


def pretty_list(request):
    """靓号列表"""

    ### 查找
    data_dict = {}  # 设一个空字典
    value = request.GET.get("res1", "")
    if value:  # 用户通过url传入关键字，只有输入了关键字不为空了，才往字典里写入这个值
        # data_dict = {"mobile__contains": value}
        data_dict['mobile__contains'] = value

    # 然后根据关键字查询
    res = models.PrettyNum.objects.filter(**data_dict)
    print(res)

    """分页（老方法）"""
    # 1.根据用户想要的页码，计算出起止位子
    page = int(request.GET.get('page', 1))
    page_size = 5  # 设置每一页显示数据的条数
    start = (page - 1) * page_size
    end = page * page_size
    # select * from 表 order by id asc（正序）/desc（倒序）
    # order_by(-level")":倒序排列，  order_by("level"):正序排列

    queryset1 = models.PrettyNum.objects.filter(**data_dict).all().order_by("-level")[start: end]

    # 根据数据库里的数据，生成页码的个数
    # total_count: 数据的总条数
    total_count = models.PrettyNum.objects.filter(**data_dict).all().order_by(
        "-level").count()  # 数据库中符合筛选条件的数据有多少条，就把条数附给total_count

    # 计算出总页码
    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count = total_page_count + 1
    print(total_page_count, div)

    # # 计算出，显示当前页的前5页，后5页
    # plus = 5
    # start_page = page - plus
    # end_page = page + plus

    # 页码
    page_str_list = []

    # 上一页
    if page > 1:
        prev = '<li ><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        # 当到达1时，固定为1不变
        prev = '<li ><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)

    for i in range(1, total_page_count + 1):  # range是前取后不取，所以要➕1
        if i == page:
            # 每次循环生成一个li
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        # 将生成的li添加到page_str_list列表中
        page_str_list.append(ele)

    # 下一页
    if page < total_page_count:
        prev = '<li ><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        # 当等于总页数时，不应该有下一页，此时写死
        prev = '<li ><a href="?page={}">下一页</a></li>'.format(total_page_count)
    page_str_list.append(prev)

    # 查询页码
    search_string = """
            <form method="get" style=";float: left;margin-left: 0px">
            <div class="input-group" style="width: 130px; height">
                <input style="height: 42px" type="text" name="page" class="form-control" placeholder="页码">
                <span class="input-group-btn">
                    <button style="height: 42px"  class="btn btn-default" type="submit">跳转</button>
                </span>
            </div>
            </form>
    """
    page_str_list.append(search_string)

    # 把分好页的数据返回到前端页面
    # page_string = "".join(page_str_list)    # 这里返回的是字符串，并不是html中的li语句，所以我们要用mark_safe包装html标签
    page_string = mark_safe("".join(page_str_list))

    return render(request, "pretty_list.html", {'queryset1': queryset1, "value1": value, "page_string": page_string})


from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class PrettyModelForm(forms.ModelForm):  # 专门写一个ModelForm类
    # 验证方式1
    mobile = forms.CharField(
        label="手机号",
        # 运用正则表达式:^:代表正则表达式的开头，$: 代表正则表达式的结尾
        # r'^1[3-9\d{9}$':表示以“1”开头，后面跟着一个数其范围为3~9,最后再跟9个数（一共11个数）
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号输入错误')]

    )

    class Meta:
        model = models.PrettyNum

        # fields = ['mobile', "price", "level", "status"]
        # exclude = ["level"]   # 排除level字段
        fields = "__all__"  # 表示所有的字段

    # 使用插件定义属性
    # widgets = {
    #     # 生成input标签,然后自己定义一个class=form-control（<input type="text" class="form-control">）
    #     "name": forms.TextInput(attrs={"class": "form-control"}),
    #     # 生成input标签,然后自己定义一个class=form-control（<input type="password" class="form-control">）
    #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
    #     "age": forms.TextInput(attrs={"class": "form-control"}),
    #     "account": forms.TextInput(attrs={"class": "form-control"}),
    #     "create_date": forms.TextInput(attrs={"class": "form-control"}),
    #     "gender": forms.Select(attrs={"class": "form-control"}),
    #     "depart": forms.Select(attrs={"class": "form-control"})
    #
    # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加了class="form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证方式2
    # def clean_mobile(self):
    #
    #     txt_mobile = self.cleaned_data["mobile"]
    #
    #     if len(txt_mobile) != 11:
    #         # 验证不通过
    #         raise ValidationError("格式错误")
    #     # 验证通过：把用户输入的值返回
    #     return txt_mobile


def pretty_add(request):
    """新建靓号"""

    if request.method == "GET":
        form = PrettyModelForm()  # 实例化类的对象
        return render(request, "pretty_add.html", {"form": form})  # 通过render将对象传入到HTML中。
    else:
        form = PrettyModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/pretty/list/")
        return render(request, "pretty_add.html", {"form": form})  # 通过render将对象传入到HTML中。


class PrettyEditModelForm(forms.ModelForm):  # 专门写一个只有“价格，水平，状态”的ModelForm类
    # 重新定义price数据，改成“不允许更改”
    price = forms.IntegerField(disabled=True, label="价格")

    class Meta:
        model = models.PrettyNum

        fields = ["price", "level", "status"]  # 无mobile
        # exclude = ["level"]   # 排除level字段
        # fields = "__all__"  # 表示所有的字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有插件，添加了class="form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def pretty_edit(request):
    """编辑靓号"""
    # 根据nid1获取当前对象
    nid2 = request.GET.get("nid1")
    row_object = models.PrettyNum.objects.filter(id=nid2).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form": form})

    # POST方式提交：
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request):
    """删除靓号"""
    nid2 = request.GET.get("nid1")
    models.PrettyNum.objects.filter(id=nid2).delete()
    return redirect("/pretty/list/")
