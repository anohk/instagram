# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 07:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0002_myuser_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='myuser',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female')], default=django.utils.timezone.now, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]