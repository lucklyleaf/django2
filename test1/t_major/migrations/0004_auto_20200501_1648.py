# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-01 08:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_major', '0003_auto_20200501_1647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoreinfo',
            name='sdata',
            field=models.DateField(verbose_name='\u8003\u8bd5\u65f6\u95f4'),
        ),
    ]
