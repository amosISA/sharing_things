# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-01 09:10
from __future__ import unicode_literals

from django.db import migrations, models
import posts.validators


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0013_auto_20171001_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=250, validators=[posts.validators.validate_title]),
        ),
    ]
