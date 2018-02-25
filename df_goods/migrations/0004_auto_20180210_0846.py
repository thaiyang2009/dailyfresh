# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-10 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0003_slide'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atitle', models.CharField(default='', max_length=100)),
                ('aalt', models.CharField(default='', max_length=100)),
                ('apic', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.AlterField(
            model_name='slide',
            name='spic',
            field=models.ImageField(upload_to='images'),
        ),
    ]