# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-20 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodroller', '0007_auto_20151220_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
