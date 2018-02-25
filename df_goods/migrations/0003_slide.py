# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-10 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0002_typeinfo_tshow'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stitle', models.CharField(default='', max_length=100)),
                ('salt', models.CharField(default='', max_length=100)),
                ('spic', models.ImageField(upload_to='static/images')),
            ],
        ),
    ]
