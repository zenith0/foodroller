# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodroller', '0008_auto_20151220_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='category',
            field=models.ManyToManyField(related_name='food', to='foodroller.Category'),
        ),
    ]
