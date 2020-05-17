# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.contrib import admin


@admin.register(TeacherInfo)
class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'tnum', 'tname', 'tpwd', 'tsex','tnumber','is_banzhuren']
    list_editable = ['tnum', 'tname', 'tpwd', 'tsex', 'is_banzhuren','tnumber']
    list_per_page = 15
    list_filter = ['tnum', 'tsex']
    search_fields = ['tnum']


@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cname']
    list_editable = ['cname']
    list_per_page = 15


@admin.register(GradeInfo)
class GradeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'clname']
    list_editable = ['clname']
    list_per_page = 15


@admin.register(TeachInfo)
class TeachInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'teacher', 'course', 'grade']
    list_editable = ['teacher', 'course', 'grade']
    list_per_page = 15


admin.site.site_header = "成绩管理"
