# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 03:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20170217_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostUserVisibleManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]