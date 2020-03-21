# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from . import user_decorator
from df_goods import *
import df_order
from django.core.paginator import *


def register(request):
    context = {'title': '用户注册'}
    return render(request, 'df_user/register.html', context)


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 加密
    s1 = sha1()
    s1.update(upwd)
    upwd = s1.hexdigest()

    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd
    user.uemail = uemail
    user.save()

    # 注册成功，转到登录页面
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    cookie = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'uname': cookie, 'error_name': 0, 'error_pwd': 0}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    users = UserInfo.objects.filter(uname=uname)

    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd:
            url = request.COOKIES.get('url', '/user/info')
            red = HttpResponseRedirect(url)
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/user/login')


@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    # 当goods_ids为空时，‘’会导致int（goods_id）转化失败，从而报错
    if goods_ids != '':
        for goods_id in goods_ids1:
            goods_list.append(models.GoodsInfo.objects.get(id=int(goods_id)))
    context = {
        'title': '用户中心', 'page_name': 1,
        'user_email': user_email,
        'user_name': request.session['user_name'],
        'goods_list': goods_list
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request, index):
    user_ids = request.session['user_id']
    order1 = df_order.models.OrderInfo.objects.filter(user_id=user_ids).order_by('oIspay')
    id = [item.oid for item in order1]
    orderdetail = df_order.models.OrderDetailInfo.objects.filter(order_id__in=id)
    paginator = Paginator(order1, 2)
    if index == '':
        index = 1
    page = paginator.page(int(index))
    context = {'title': '我的订单', 'page_name': 1,
               'paginator': paginator, 'page': page,
               'orderdetail': orderdetail}
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request, id):
    if id:
        request.session['id'] = id
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
        context = {'title': '收货地址','user': user, 'page_name': 1, 'id': id}
        print ('------------------------>%s' % id)
        if request.session.has_key('id'):
            del request.session['id']
            return HttpResponseRedirect('/df_order/')
        else:
            return render(request, 'df_user/user_center_site.html', context)
    context = {'title': '收货地址', 'user': user, 'page_name': 1, 'id': id}
    return render(request, 'df_user/user_center_site.html', context)