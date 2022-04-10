"""programGit URL Configuration

The `urlpatterns` list routes URLs to views01. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views01
    1. Add an import:  from my_app import views01
    2. Add a URL to urlpatterns:  path('', views01.home, name='home')
Class-based views01
    1. Add an import:  from other_app.views01 import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app02 import views
from app02.views01 import depart
from app02.views01 import pretty
from app02.views01 import user
from app02.views01 import admin


urlpatterns = [
    # path('admin/', admin.site.urls),
    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/modelform_add/', user.user_modelform_add),
    # 修改
    path('user/<int:nid>/edit/', user.user_edit),
    path('user/edit/', user.user_edit),
    # 删除
    path('user/delete/', user.user_delete),

    # 靓号管理
    path('pretty/list/', pretty.pretty_list),
    # 添加
    path('pretty/add/', pretty.pretty_add),
    # 编辑
    path('pretty/edit/', pretty.pretty_edit),
    # 删除
    path('pretty/delete/', pretty.pretty_delete),

    # 管理员管理
    path('admin/list/', views.admin_list),
    path('admin/add/', views.admin_add),
    path('admin/edit/', views.admin_edit),
    path('admin/delete/', views.admin_delete),

    # 登录
    path('login/', views.login)
]

