#!/usr/bin/env python
# coding:utf-8

from django.utils.http import urlquote
from django.shortcuts import redirect, resolve_url
from . import models

def require_login(func):

    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')

        if user_id:
            user_obj = models.UserInfo.objects.get(pk=user_id)
            request.df_user = user_obj
            return func(request, *args, **kwargs)
        else:
            next_url = request.get_full_path()
            url = '?'.join([resolve_url('login'), 'next_url=%s' % urlquote(next_url)])
            return redirect(url)

    return wrapper


def get_user(func):

    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id')

        if user_id:
            user_obj = models.UserInfo.objects.get(pk=user_id)
            request.df_user = user_obj
        else:
            request.df_user = None
        return func(request, *args, **kwargs)

    return wrapper