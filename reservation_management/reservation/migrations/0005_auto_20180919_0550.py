# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-19 05:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_auto_20180919_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.BigIntegerField(default=1537336220),
        ),
    ]
