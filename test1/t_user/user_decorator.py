#coding=utf-8
from django.http import HttpResponseRedirect


# 如果未登录则转到登录页面
def login(func):
    def login_fun(request, *args, **kwargs):
        if request.session.has_key('num'):
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/t_user')
    return login_fun