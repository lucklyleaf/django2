# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class TeacherInfo(models.Model):
    choice = [
        (1, '男'),
        (2, '女')
    ]
    list_choice = list(choice)
    tnum = models.CharField(max_length=10, unique=True, verbose_name='编号')
    tname = models.CharField(max_length=20, verbose_name='姓名')
    tpwd = models.CharField(max_length=60, verbose_name='密码')
    tsex = models.IntegerField(default=1, choices=list_choice, verbose_name='性别')
    tnumber = models.CharField(max_length=13, verbose_name='联系方式',blank=True)
    is_banzhuren = models.BooleanField(default=False, verbose_name='是否为班主任')

    def __str__(self):
        return self.tname.encode('utf-8')

    class Meta:
        verbose_name_plural = '教师信息'
        verbose_name = '教师信息'


class CourseInfo(models.Model):
    cname = models.CharField(max_length=10, unique=True, verbose_name='科目')

    def __str__(self):
        return self.cname.encode('utf-8')

    class Meta:
        verbose_name_plural = '课程信息'
        verbose_name = '课程信息'


class GradeInfo(models.Model):
    choice = [
        (1, '理科'),
        (2, '文科')
    ]
    list_choice = list(choice)
    clname = models.CharField(max_length=10, unique=True, verbose_name='班级')
    clnature = models.IntegerField(choices=list_choice, verbose_name='班级性质')

    def __str__(self):
        return self.clname.encode('utf-8')

    class Meta:
        verbose_name_plural = '班级信息'
        verbose_name = '班级信息'


class TeachInfo(models.Model):
    teacher = models.ForeignKey(TeacherInfo, verbose_name='教师姓名')
    grade = models.ForeignKey(GradeInfo, verbose_name='所带班级')
    course = models.ForeignKey(CourseInfo, verbose_name='所带课程')

    class Meta:
        verbose_name_plural = '教师任课'
        verbose_name = '教师任课'