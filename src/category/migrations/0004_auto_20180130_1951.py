# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-30 12:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0003_auto_20180130_1943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='news',
            new_name='category',
        ),
    ]
