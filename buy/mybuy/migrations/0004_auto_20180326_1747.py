# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-26 17:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mybuy', '0003_auto_20180326_1745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='lable',
            new_name='name',
        ),
    ]
