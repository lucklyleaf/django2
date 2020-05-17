# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class StudentInfo(models.Model):
    choice = (
        (1, '男'),
        (2, '女'),
        (3, '其他')
    )
    list_choice = list(choice)
    snum = models.CharField(max_length=20, primary_key=True, unique=True, verbose_name='学号')
    sname = models.CharField(max_length=10, verbose_name='姓名')
    ssex = models.IntegerField(choices=choice, verbose_name='性别')
    grade = models.ForeignKey('t_user.GradeInfo', verbose_name='班级')

    class Meta:
        verbose_name_plural = '学生信息'
        verbose_name = '学生信息'

    def __str__(self):
        return self.snum.encode('utf-8')


class ScoreInfo(models.Model):
    choice = [
        (1, '平时成绩'),
        (2, '期中成绩'),
        (3, '期末成绩'),
        (4, '模拟成绩'),
        (5, '其他成绩')
    ]
    list_choice = list(choice)
    snum = models.ForeignKey(StudentInfo, verbose_name='学号')
    scourse = models.ForeignKey('t_user.CourseInfo', verbose_name='课程')
    sscore = models.IntegerField(verbose_name='考试成绩', null=True,blank=True)
    stype = models.IntegerField(choices=list_choice, verbose_name='考试类型')
    sdata = models.DateField(verbose_name='考试时间')

    class Meta:
        verbose_name_plural = '成绩信息'
        verbose_name = '成绩信息'