# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-29 18:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mybuy', '0008_buy_list_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy_good',
            name='good',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mybuy.Good'),
        ),
        migrations.AlterField(
            model_name='buy_good',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]