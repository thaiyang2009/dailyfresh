# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-09 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gtitle', models.CharField(max_length=20)),
                ('gpic', models.ImageField(upload_to='df_goods')),
                ('gprice', models.DecimalField(decimal_places=2, max_digits=5)),
                ('gunit', models.CharField(default='500g', max_length=20)),
                ('gclick', models.IntegerField(default=0)),
                ('gsummary', models.CharField(max_length=256)),
                ('gstorage', models.IntegerField()),
                ('gcontent', tinymce.models.HTMLField()),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TagInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tname', models.CharField(max_length=20, unique=True)),
                ('ttime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ttitle', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtags',
            field=models.ManyToManyField(blank=True, to='df_goods.TagInfo'),
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='df_goods.TypeInfo'),
        ),
    ]
