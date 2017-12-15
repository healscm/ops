# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-04 05:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20171203_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='apply_time',
            field=models.CharField(max_length=30, null=True, verbose_name='提交时间'),
        ),
        migrations.AddField(
            model_name='task',
            name='finish_time',
            field=models.CharField(max_length=30, null=True, verbose_name='完成时间'),
        ),
    ]