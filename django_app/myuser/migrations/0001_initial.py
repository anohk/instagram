# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Myuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='user name')),
                ('last_name', models.CharField(max_length=50, verbose_name='last name')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('nickname', models.CharField(max_length=50, verbose_name='nickname')),
                ('email', models.EmailField(max_length=100, verbose_name='email')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('following', models.ManyToManyField(related_name='follower_set', to='myuser.Myuser')),
            ],
        ),
    ]
