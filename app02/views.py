from django.http import HttpResponse
from django.shortcuts import render, redirect
from app02.utils.pagination import Pagination
from app02 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

# Create your views01 here.
"""部门管理"""


def depart_list(request):
    """部门列表"""

    depart = models.Department.objects.all()
    return render(request, "depart_list.html", {'department': depart})


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, "depart_add.html")

    # 获取用户POST提交过来的数据
    title = request.POST.get("title")

    # 保存到数据库
    models.Department.objects.create(title=title)

    # 重定向回部门列表页面
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    # 用GET方式获取URL传来的值
    nid2 = request.GET.get("nid1")
    # 删除
    models.Department.objects.filter(id=nid2).delete()
    # 重定向回部门列表
    return redirect("/depart/list/")


def depart_edit(request):
    """修改部门"""
    if request.method == "GET":
        nid2 = request.GET.get("nid1")
        # 编辑第一行对象
        row_object = models.Department.objects.filter(id=nid2).first()
        print(row_object.id, row_object.title)
        # 把row_object对象传递到html中，然后html调用里面的参数
        return render(request, 'depart_edit.html', {"row_object": row_object})

    else:

        nid2 = request.GET.get("nid1")
        # 获取用户提交的标题
        title = request.POST.get("title")
        # 根据id找到数据库中的数据并进行更新
        models.Department.objects.filter(id=nid2).update(title=title)
        # 重定向回部门列表
        return redirect("/depart/list/")


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
        'queryset1': page_object.page_queryset,  # 分完页的数据
        'page_string': page_object.html(),  # 生成的页码
        'value1': value
    }
    return render(request, "admin_list.html", context)


class AdminModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username", "password"]
        widgets = {
            "password": forms.PasswordInput()  # 设为密码输入框，可以隐藏密码
        }


def admin_add(request):
    """管理员添加"""
    if request.method == "GET":

        form = AdminModelForm()
        return render(request, 'admin_modelform_add.html', {"form1": form})
    else:
        form = AdminModelForm(data=request.POST)  # 接收用户输入的值
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




def login(request):
    """登录"""
    if request.method == "POST":
        # 提取html页面传过来的姓名和密码
        username2 = request.POST.get('username1')
        password2 = request.POST.get('password1')
        # 如果用户名正确则进行下一步
        if models.User.objects.filter(name=username2):
            if models.User.objects.filter(name=username2)[0].password == password2:
                # 如果密码正确则转向新页面
                row_object = models.User.objects.filter(name=username2).first()
                return render(request, 'depart_list.html', {'row_object':row_object})
            else:
                # 否则继续登录
                return render(request, 'login.html')
        else:
            HttpResponse("用户不存在")
    return render(request, "login.html")


