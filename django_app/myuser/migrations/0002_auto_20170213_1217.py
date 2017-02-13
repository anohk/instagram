# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 03:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(blank=True, max_length=100, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='follower_set', to='myuser.Myuser'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='nickname',
            field=models.CharField(max_length=30, verbose_name='nickname'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='user name'),
        ),
    ]
