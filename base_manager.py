#!/usr/bin/env python
# coding:utf-8

from django.db import models

class BaseManager(models.Manager):
    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(isDelete=False)
