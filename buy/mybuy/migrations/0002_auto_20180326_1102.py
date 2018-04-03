# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-26 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybuy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buy_good',
            name='good',
        ),
        migrations.RemoveField(
            model_name='buy_list',
            name='client',
        ),
        migrations.RemoveField(
            model_name='buy_list',
            name='pay',
        ),
        migrations.AddField(
            model_name='buy_good',
            name='good_name',
            field=models.CharField(blank=True, max_length=160, null=True),
        ),
        migrations.AddField(
            model_name='buy_good',
            name='good_photo',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='buy_list',
            name='client_name',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='buy_list',
            name='client_phone',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AddField(
            model_name='buy_list',
            name='client_site',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='buy_good',
            name='good_specification',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=36),
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='client_site',
            name='site',
            field=models.CharField(blank=True, max_length=210, null=True),
        ),
        migrations.AlterField(
            model_name='good',
            name='name',
            field=models.CharField(max_length=160),
        ),
        migrations.AlterField(
            model_name='good',
            name='remark',
            field=models.CharField(max_length=740),
        ),
        migrations.AlterField(
            model_name='good_lable',
            name='lable',
            field=models.CharField(max_length=36),
        ),
    ]