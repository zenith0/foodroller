# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodroller', '0012_auto_20160103_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='thumb',
            field=models.ImageField(blank=True, null=True, upload_to='img'),
        ),
    ]
