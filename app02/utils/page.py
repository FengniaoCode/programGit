# -*- coding:utf-8 -*-
"""
----------------------------------------------------------
作者: 武广辉
日期: 2022/4/1 16:58
----------------------------------------------------------
当前项目的名称: 自定义分页组件
在文件创建过程中在“新建文件”对话框中指定的新文件的名称: page.py
当前集成开发环境: PyCharm
----------------------------------------------------------
"""
class Pageination(object):

    def __init__(self, request, page_param="page"):
        page = request.GET.get(page_param, 1)   #
        if page.isdecimal():
            page = int(page)
        else:
            page = 1