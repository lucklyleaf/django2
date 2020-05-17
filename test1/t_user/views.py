# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Q
from models import *


def login(request):
    cookie = request.COOKIES.get('user', '')
    context = {'title': '用户登录', 'user': cookie,}
    return render(request, 't_user/login.html', context)


def login_handle(request):
    num = request.POST.get('user')
    pwd = request.POST.get('pwd')
    code = request.POST.get('code')
    jizhu = request.POST.get('jizhu', '0')
    users = TeacherInfo.objects.filter(Q(tnum=num) & Q(tpwd=pwd))
    er = ''
    us = dict()
    for u in users:
        us['is_banzhuren'] = u.is_banzhuren
    code1 = request.session.get('code')
    if str.strip(code.encode('utf-8')) == str.strip(code1.encode('utf-8')):
        if len(users) == 1:
            if us['is_banzhuren']:
                red = HttpResponseRedirect('/banzhuren')
            else:
                red = HttpResponseRedirect('/ordinary/1')
            if jizhu != 0:
                red.set_cookie('user', num)
            else:
                red.set_cookie('user', '', max_age=-1)
            request.session['num'] = num
            return red
        else:
            context = {'error_user': 1, 'error_yan': 2, 'title': '用户登录', 'user': num, 'pwd': pwd,'users':users}
            return render(request, 't_user/login.html', context)
    else:
        context ={'code':  code, 'code1': code1, 'error_yan': 1, 'error_user': 2, 'title': '用户登录', 'user':num, 'pwd': pwd}
        return render(request, 't_user/login.html', context)


# 验证码
def verifyCode(request):
    from PIL import Image, ImageDraw, ImageFont
    import random
    # 背景颜色
    bgColor = (random.randrange(50, 150), random.randrange(50, 100), 0)
    # 高宽
    width = 100
    height = 25
    # 创建画布
    image = Image.new('RGB', (width, height), bgColor)
    # 构建字体对象
    font = ImageFont.truetype('FreeMono.ttf', 24)
    # 创建画笔
    draw = ImageDraw.Draw(image)
    # 创建文本内容
    import string
    text1 = string.letters+string.digits
    # 逐个绘制字符
    textTemp = ' '
    for t1 in range(4):
        textTemp1 = text1[random.randrange(0, len(text1))]

        draw.text((t1 * 25, 0),
                  textTemp1,
                  (255, 255, 255), font)
        textTemp += textTemp1
    request.session['code'] = textTemp
    # draw.text((0, 0), text, (255, 255, 255), font)
    # 保存到内存流中
    import cStringIO
    buf = cStringIO.StringIO()
    image.save(buf, 'png')
    # 将内存流中的内容输出到客户端
    return HttpResponse(buf.getvalue(), 'images/png')