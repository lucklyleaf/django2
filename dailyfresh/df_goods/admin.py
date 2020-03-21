# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *
from django.contrib import admin


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'gtitle', 'gpic', 'gprice', 'gunit', 'gclick', 'gkucun', 'isDelete', 'gjianjie', 'gcontent', 'gtype' ]


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
