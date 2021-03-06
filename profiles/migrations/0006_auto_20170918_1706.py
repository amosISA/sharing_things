# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-18 15:06
from __future__ import unicode_literals

from django.db import migrations, models
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20170909_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='posts/img/favicon/fav.png', height_field='height_field', null=True, upload_to=profiles.models.upload_location, width_field='width_field'),
        ),
    ]
