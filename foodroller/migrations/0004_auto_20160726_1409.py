# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-26 14:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodroller', '0003_foodplan_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodplan',
            options={'ordering': ['start_date']},
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
