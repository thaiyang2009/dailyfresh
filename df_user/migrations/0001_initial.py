# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-09 08:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=20, unique=True)),
                ('_upwd', models.CharField(max_length=40)),
                ('uemail', models.EmailField(default='', max_length=254, unique=True)),
                ('ushou', models.CharField(default='', max_length=30)),
                ('uaddress', models.CharField(default='', max_length=100)),
                ('uyoubian', models.CharField(default='', max_length=6)),
                ('uphone', models.CharField(default='', max_length=11)),
            ],
        ),
    ]