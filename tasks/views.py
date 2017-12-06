#!/usr/bin/env python
# encoding: utf-8
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
import json
import datetime
import io
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from tasks.forms import *
from ops.common import *

@login_required()
def task_list(request):
    """
       组列表
       :param request:
       :return:
       """
    header_title, sub_title, path1, path2 = "", "", "任务系统", "任务管理"
    # return render_to_response('user/group_list.html', locals())
    return render(request, 'tasks/task_list.html', locals())

@login_required()
def task_search(request):
    """
       组列表
       :param request:
       :return:
       """
    header_title, sub_title, path1, path2 = "", "", "任务管理", "查询任务"
    return render(request, 'tasks/task_search.html', locals())

@login_required()
def task_detail(request):
    """
       组列表
       :param request:
       :return:
       """
    header_title, sub_title, path1, path2 = "", "", "任务管理", "测试任务"
    task_all = Task.objects.all()
    return render(request, 'tasks/task_detail.html', locals())



@login_required()
def get_tasklist(request):
    """
    获取任务列表
    """
    offset = request.GET.get('offset', None)
    limit = request.GET.get('limit', None)
    sort = request.GET.get('sort', None)
    keywords = request.GET.get('search', None)

    if sort is None:
        sort = "id"

    order = request.GET.get('order', None)
    if order == "desc":
        sort = "-task_name"
    count = Task.objects.all().count()
    # group_list = UserGroup.objects.all()[int(offset):int(offset + limit)]
    task_list = Task.objects.order_by(sort).all()[int(offset):int(offset + limit)]
    if keywords:
        task_list = Task.objects.order_by(sort).filter(
            Q(name__icontains=keywords) | Q(comment__icontains=keywords))[int(offset):int(offset + limit)]
    rows = [
        {
            'id': g.id,
            'task_name': g.task_name,
            'task_type': g.task_type,
            'task_desc': g.task_desc,
            'task_applyer_name': g.task_applyer_name,
            'task_approve_name': g.task_approve_name,
            'task_executer': g.task_executer,
            'apply_time': g.apply_time,
            'finish_time': g.finish_time,
            'is_finished': g.is_finished,
        } for g in task_list]
    data = {'total': count, 'rows': rows}
    return JsonResponse(data)



@login_required()
def task_add(request):
    """
       添加任务
       :param request:
       :return:
       """
    task_types = TASK_TYPE
    header_title, sub_title, path1, path2 = "", "", "任务系统", "创建任务"
    task_all = Task.objects.all()
    if request.method == 'POST':
        task_form = TaskModelForm(request.POST)
        ret = {'code': 0, 'message': ''}
        task_name = request.POST.get('task_name', '')
        task_type = request.POST.get('task_type', '')
        task_desc = request.POST.get('task_desc', '')
        task_applyer_name = request.user.username
        apply_time = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')
        is_finished = 0
        task = Task(task_name=task_name, task_type=task_type, task_desc=task_desc, apply_time=apply_time, task_applyer_name=task_applyer_name, is_finished=is_finished)
        task.save()
    else:
        task_form = TaskModelForm()

    return render(request, 'tasks/task_add.html', locals())
    return HttpResponseRedirect(reverse(task_list))



@login_required()
def task_del(request):
    """
       查看任务列表
       :param request:
       :return:
       """
    header_title, sub_title, path1, path2 = "", "", "任务管理", "删除任务"
    ret = {'Code': 0, 'Message': ''}
    if request.method == 'POST':
        # for key in request.POST:
        #     print(key)
        #     valuelist = request.POST.getlist(key)
        #     print(valuelist)
        ret = {'code': 0, 'message': ''}
        if request.method == 'POST':
            ids = request.POST.getlist('ids[]')
            for id in ids:
                Task.objects.get(id=id).delete()
                ret['code'] = 1
                ret['message'] = '执行成功'
        return HttpResponse(json.dumps(ret))

@login_required()
def task_edit(request):
    """
       编辑任务
       查看详情
       :param request:
       :return:
       """
    # task_all = Task.objects.all()
    if request.method == 'GET':
        task_id = request.GET.get('id', None)
        task = Task.objects.get(id=task_id)
        # TODO:获取表单错误信息
        # print(form.errors）
        return render(request, 'tasks/task_edit.html', locals())



@login_required()
def task_success(request):
    """
       审批通过任务
       :param request:
       :return:
       """
    # task_all = Task.objects.all()
    ret = {'Code': 0, 'Message': ''}
    if request.method == 'POST':
        # for key in request.POST:
        #     print(key)
        #     valuelist = request.POST.getlist(key)
        #     print(valuelist)
        ids = request.POST.getlist('ids[]')
        for id in ids:
            if Task.objects.get(id=id).is_finished == '1':
                ret['code'] = 0
                ret['message'] = '该任务已审批'
                continue
            else:
                finish_time = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')
                task_approve_name = request.user.username
                is_finished = 1
                Task.objects.filter(id=id).update(finish_time=finish_time, task_approve_name=task_approve_name, is_finished=is_finished)
                ret['code'] = 1
                ret['message'] = '执行成功'
    return HttpResponse(json.dumps(ret))


@login_required()
def task_refuse(request):
    """
       拒绝任务
       :param request:
       :return:
       """
    # task_all = Task.objects.all()
    if request.method == 'GET':
        task_id = request.GET.get('id', None)
        task = Task.objects.get(id=task_id)
        # TODO:获取表单错误信息
        # print(form.errors)
        finish_time = datetime.datetime.now().strftime('%Y/%m/%d-%H:%M')
        task_approve_name = request.user.username
        Task.objects.filter(id=task_id).update(finish_time=finish_time, task_approve_name=task_approve_name)
        return render(request, 'tasks/task_edit.html', locals())

@login_required()
def task_myself(request):
    """
       组列表
       :param request:
       :return:
       """
    header_title, sub_title, path1, path2 = "", "", "任务管理", "我的申请"
    task_all = Task.objects.all()
    return render(request, 'tasks/task_myself.html', locals())

@login_required()
def task_todo(request):
    """
       组列表
       :param request:
       :return:
       """
    header_title, sub_title, path1, path2 = "", "", "任务管理", "待办任务"
    task_all = Task.objects.all()
    return render(request, 'tasks/task_todo.html', locals())