# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-27 12:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodroller', '0010_auto_20160927_1203'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('user', 'slug')]),
        ),
    ]
