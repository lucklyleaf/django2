# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.contrib import admin


@admin.register(StudentInfo)
class StudentInfoAdmin(admin.ModelAdmin):
    list_display = ['snum', 'sname', 'ssex', 'grade']
    list_per_page = 15
    list_editable = ['sname', 'ssex', 'grade']
    list_filter = ['ssex', 'grade']
    search_fields = ['sname']


@admin.register(ScoreInfo)
class ScoreInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'snum', 'scourse', 'sscore', 'stype', 'sdata']
    list_per_page = 15
    list_editable = ['snum', 'scourse', 'sscore', 'stype', 'sdata']
    list_filter = ['scourse',  'stype']
    search_fields = ['snum__snum']
