# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 21:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20170919_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
