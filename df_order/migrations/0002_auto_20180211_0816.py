# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-11 08:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('df_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-ctime']},
        ),
        migrations.AddField(
            model_name='order',
            name='ctime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
