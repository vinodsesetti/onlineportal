# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-18 05:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='numbers',
            new_name='number',
        ),
    ]
