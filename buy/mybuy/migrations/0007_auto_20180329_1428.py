# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-29 14:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybuy', '0006_auto_20180327_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='gathering',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='good_specification',
            name='specificati',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]