# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-01 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gradeinfo',
            name='clnature',
            field=models.IntegerField(choices=[(1, '\u7406\u79d1'), (2, '\u6587\u79d1')], default=1, verbose_name='\u73ed\u7ea7\u6027\u8d28'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='teacherinfo',
            name='tsex',
            field=models.BooleanField(default=True, verbose_name='\u6027\u522b'),
        ),
    ]
