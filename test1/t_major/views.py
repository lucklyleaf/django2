# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from models import *
import t_user
from t_user import user_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max, F, Q, Avg, Sum, Max, Min, Count
from django.core.paginator import *
from datetime import datetime, date


def index(request):
    if request.method == 'POST':
        xuehao = request.POST.get('xuehao', '')
        if xuehao != '':
            uname = StudentInfo.objects.get(snum=xuehao)
            num = t_user.models.GradeInfo.objects.get(clname=uname.grade)
            result = ScoreInfo.objects.filter(Q(snum=xuehao) & Q(stype__in=[2, 3, 4])).order_by('sdata')
            G = dict()
            for c in result:
                import sys
                reload(sys)
                sys.setdefaultencoding('utf8')
                G.setdefault(c.sdata, {}).update({'%s'.decode('unicode_escape') % c.scourse: c.sscore, 'type': c.stype})
            # 由于G是字典，而字典无序的，此处字典转化为list，以便排序
            h = list(G.items())
            h.sort(reverse=True)
            content = {'xuehao': xuehao, 'uname':uname, 'num': num, 'G': G, 'result': result,'h':h}
            return render(request, 't_major/index.html', content)
    return render(request, 't_major/index.html')


@csrf_exempt
@user_decorator.login
def ordinary(request, pindex):
    num = request.session.get('num')
    user = t_user.models.TeacherInfo.objects.filter(tnum=num)
    users = t_user.models.TeacherInfo.objects.get(tnum=num)
    username = user[0].tname
    banji = t_user.models.TeachInfo.objects.filter(teacher=user[0].id).order_by('grade')
    cl = ''
    bj = list()
    for b in banji:
        bj.append(b.grade)
    # bj.sort(reverse=True)
    import sys
    defaultencoding = 'utf-8'
    if sys.getdefaultencoding() != defaultencoding:
        reload(sys)
        sys.setdefaultencoding(defaultencoding)
    if request.method == 'GET':
        d = banji[0].grade
        print (d)
        co = banji[0].course
        cl = d
        print ('------------------------>%s'% cl)
    else:
        print ('------------------>%s'%request.POST.get('grade'))
        cl = request.POST.get('grade')
        d = t_user.models.GradeInfo.objects.get(clname=cl).id
        print ('------------------>%s' % d)
        c = t_user.models.TeachInfo.objects.filter(Q(teacher=user[0].id) & Q(grade=d))
        co = c[0].course
        print ('------------------>%s' % co)
    num = StudentInfo.objects.filter(grade=d)
    print (num)
    ls = list()
    for i in num:
        ls.append(i.snum)
    result = ScoreInfo.objects.filter(Q(snum__in=ls) & Q(scourse=co)).order_by('-sdata')
    print (result)
    G = dict()
    for r in result:
        source = ScoreInfo.objects.filter(Q(snum__in=ls) & Q(scourse=co) & Q(sdata=r.sdata))
        pg = source.aggregate(avg=Avg('sscore'))
        #  pg = source.annotate(avg=Avg('sscore'))
        #  p = list(pg)
        #  h = ''
        #  for i in p:
        #      h = i.avg
        #      print ("----------------%s"%i.avg)
        c_avg = ScoreInfo.objects.filter(Q(snum__in=ls) & Q(scourse=co) & Q(sdata=r.sdata)).filter(sscore__gt=pg['avg'])
        count = source.count
        G.setdefault(r.sdata, {}).update({'gtype': r.stype,
                                          'data': r.sdata,
                                          'km': r.scourse,
                                          'avg': pg,
                                          'c_avg': c_avg.count,
                                          'count': count})
    h = list(G.items())
    h.sort(reverse=True)
    # 将排序后的h进行分页
    paginator = Paginator(h, 4)
    page = paginator.page(int(pindex))
    print(page)
    content = {'username': username, 'page': page,
        'paginator': paginator, 'title': '教师主页','banji': bj,'h':h, 'cl': cl, 'users': users}
    return render(request, 't_major/t_major_teacher.html', content)


@user_decorator.login
@csrf_exempt
def uqdate(request):
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    sex = request.POST.get('sex')
    number = request.POST.get('number')
    num = request.session.get('num')
    user = t_user.models.TeacherInfo.objects.get(tnum=num)
    try:
        user.tname = username
        user.tpwd = pwd
        user.tsex = sex
        user.tnumber = number
        user.save()
        data = 'ok'
    except Exception as e:
        error = '===============>>> %s' % e
        data = error
    data = {'data': data}
    return JsonResponse(data)


@csrf_exempt
@user_decorator.login
def select_source(request, pindex):
    xuehao = ''
    if request.method == 'POST':
        xuehao = request.POST.get('xuehao', '')
        request.session['xs'] = xuehao
    print('---------------->%s'%xuehao)
    xuehao = request.session.get('xs')
    print ('---------------->%s'%xuehao)

    num = request.session.get('num')
    error = ''
    user = t_user.models.TeacherInfo.objects.get(tnum=num)
    username = user.tname
    # 查询老师所带课程
    teacher_kc = t_user.models.TeachInfo.objects.filter(teacher=user.id)
    kc = list()
    H = dict()
    paginator = ''
    page = ''
    for i in teacher_kc:
        kc.append(i.grade)
    # 查询学生所在班
    classmates = StudentInfo.objects.filter(Q(sname=xuehao) | Q(snum=xuehao))
    if classmates:
        banji = classmates[0].grade
        # 判断学生是否在该老师所带的班级里
        if banji in kc:
            # 通过老师的id和学生所在班级查询课程
            renke = t_user.models.TeachInfo.objects.get(Q(grade=banji) & Q(teacher=user.id))
            # 得到该学生的所有成绩
            grade = ScoreInfo.objects.filter(Q(snum=classmates[0].snum) & Q(scourse=renke.course)).order_by('-sdata')
            ls = list()
            # 得到属于该班级的学号
            sy_xh = StudentInfo.objects.filter(grade=banji)
            for s in sy_xh:
                ls.append(s.snum)
            paginator = Paginator(grade, 5)
            page = paginator.page(int(pindex))
            for g in page:
                # 查询学生所在班级的本门课程本次考试的平均成绩和参考人数以及排名
                grade_data = ScoreInfo.objects.filter(Q(sdata=g.sdata) & Q(scourse=renke.course) & Q(snum__in=ls))
                paiming = ScoreInfo.objects.filter(Q(sdata=g.sdata) & Q(scourse=renke.course) & Q(snum__in=ls)).filter(sscore__gt=g.sscore)
                H.setdefault(g.sdata, {}).update({'xh': g.snum,
                                                  'xs':classmates[0].sname,
                                                  'kc': g.scourse,
                                                  'banji': banji,
                                                  'grade': g.sscore,
                                                  'da': g.sdata,
                                                  'type': g.stype,
                                                  'p': paiming.count,
                                                  'avg': grade_data.aggregate(Avg('sscore')),
                                                  'count': grade_data.count})
            P = list(H.items())
            P.sort(reverse=True)
        else:
            error = '所带班级没有该名学生'
    else:
        error = '没有该名学生'
    context = {'title': '成绩查询','data': H, 'page': page,
        'paginator': paginator,'error':  error, 'username': username,'P':P}
    return render(request, 't_major/teacher_select_source.html', context)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/t_user')


@user_decorator.login
def select_xiangqing(request,  pindex):
    import sys
    defaultencoding = 'utf-8'
    if sys.getdefaultencoding() != defaultencoding:
        reload(sys)
        sys.setdefaultencoding(defaultencoding)
    # 第一次进入将值存入session，以便分页提取这些值
    data = request.GET.get('data', request.session.get('data'))
    banji = request.GET.get('banji', request.session.get('banji'))
    request.session['data'] = data
    request.session['banji'] = banji
    # 将字符串2019年2月20日转换成date类型
    da = datetime.strptime(data, '%Y年%m月%d日').date()
    num = request.session.get('num')
    user = t_user.models.TeacherInfo.objects.filter(tnum=num)
    username = user[0].tname
    # 科目
    banji_id = t_user.models.GradeInfo.objects.get(clname=banji).id
    kc = t_user.models.TeachInfo.objects.get(Q(grade=banji_id) & Q(teacher=user[0].id)).course
    snum = StudentInfo.objects.filter(grade=banji_id)
    ls = list()
    for i in snum:
        ls.append(i.snum)
    cj = ScoreInfo.objects.filter(Q(sdata=da) & Q(snum__in=ls) & Q(scourse=kc)).order_by('-sscore')
    pj = cj.aggregate(avg=Avg('sscore'))
    paginator = Paginator(cj, 5)
    page = paginator.page(int(pindex))
    ll = list()
    for i in page:
        ll.append(i)
    content = {'banji': banji, 'data':data, 'title': '班级成绩',
               'username':username,'ll':ll, 'page':page,'paginator':paginator,'cj':cj,'kc':kc,'pj':pj}
    return render(request, 't_major/teacher_select_xiangqing.html', content)


@user_decorator.login
def sl_sname(request):
    snum = request.GET.get('snum')
    name = StudentInfo.objects.get(snum=snum).sname
    data = {'snum': snum,'name':name}
    return JsonResponse(data)


@user_decorator.login
def delete(request):
    a = request.GET.get('a')
    try:
        cj = ScoreInfo.objects.get(id=a)
        cj.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)


@csrf_exempt
@user_decorator.login
def cj_update(request):
    xx_id = request.POST.get('xx_id')
    xx_cj = request.POST.get('xx_cj')
    cj = ScoreInfo.objects.get(id=xx_id)
    try:
        cj.sscore = xx_cj
        cj.save()
        data = 'ok'
    except Exception as e:
        error = '===============>>> %s' % e
        data = error
    data = {'data': data}
    return JsonResponse(data)