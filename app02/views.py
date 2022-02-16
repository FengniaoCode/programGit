from django.shortcuts import render, redirect

from app02 import models


# Create your views here.
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

