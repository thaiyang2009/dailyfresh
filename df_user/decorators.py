#!/usr/bin/env python
# coding:utf-8

from django.http import HttpResponseRedirect
from django.utils.http import urlquote, urlencode, urlsafe_base64_encode
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
            print('in de next_url:', next_url)
            url = '?'.join([resolve_url('login'), 'next_url=%s' % urlsafe_base64_encode(next_url.encode()).decode()])
            print('in de url:', url)
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