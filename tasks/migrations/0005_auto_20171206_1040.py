# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-06 02:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_task_is_finshed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='is_finshed',
            new_name='is_finished',
        ),
    ]
