# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-20 14:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodroller', '0003_auto_20151220_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='duration',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='food',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='food',
            name='ingredients',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodroller.Ingredient'),
        ),
    ]
