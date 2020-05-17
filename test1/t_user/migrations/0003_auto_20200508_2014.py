# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-08 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_user', '0002_auto_20200501_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseinfo',
            options={'verbose_name': '\u8bfe\u7a0b\u4fe1\u606f', 'verbose_name_plural': '\u8bfe\u7a0b\u4fe1\u606f'},
        ),
        migrations.AlterModelOptions(
            name='gradeinfo',
            options={'verbose_name': '\u73ed\u7ea7\u4fe1\u606f', 'verbose_name_plural': '\u73ed\u7ea7\u4fe1\u606f'},
        ),
        migrations.AlterModelOptions(
            name='teacherinfo',
            options={'verbose_name': '\u6559\u5e08\u4fe1\u606f', 'verbose_name_plural': '\u6559\u5e08\u4fe1\u606f'},
        ),
        migrations.AlterModelOptions(
            name='teachinfo',
            options={'verbose_name': '\u6559\u5e08\u4efb\u8bfe', 'verbose_name_plural': '\u6559\u5e08\u4efb\u8bfe'},
        ),
        migrations.AddField(
            model_name='teacherinfo',
            name='tnumber',
            field=models.CharField(blank=True, max_length=13, verbose_name='\u8054\u7cfb\u65b9\u5f0f'),
        ),
    ]
