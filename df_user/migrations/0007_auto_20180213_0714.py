# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2018-02-13 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0006_auto_20180213_0232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='verify',
            new_name='verify_e',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='verify_p',
            field=models.BooleanField(default=False),
        ),
    ]
