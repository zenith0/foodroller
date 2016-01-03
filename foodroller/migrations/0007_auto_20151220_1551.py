# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-20 15:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodroller', '0006_auto_20151220_1532'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='ingredients',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='food',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='foodroller.Food'),
        ),
    ]