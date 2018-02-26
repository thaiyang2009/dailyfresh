#!/usr/bin/env python
# coding:utf-8

# Create your tasks here
from __future__ import absolute_import, unicode_literals
import random
import string
import logging
from django.core.cache import cache
from celery import shared_task        # 使用 shared_task 装饰器，任务可以在多个app里使用
import top.api
from dailyfresh import settings
from django.core.mail import send_mail

logger = logging.getLogger('django')
BASE_TEXT = string.ascii_uppercase + string.digits


@shared_task
def add(x, y):
    return x + y

@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)

def gen_captcha():
    choices = random.sample(BASE_TEXT, 4)
    return ''.join(choices)

@shared_task
def send_sms_captcha(phone_num):

    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(settings.ALIDAYU_KEY_ID, settings.ALIDAYU_KEY_SECRET))

    req.extend = settings.ALIDAYU_EXTEND
    req.sms_type = settings.ALIDAYU_SMS_TYPE
    req.sms_free_sign_name = settings.ALIDAYU_SMS_FREE_SIGN_NAME
    code = gen_captcha()
    req.sms_param = settings.ALIDAYU_SMS_PARAM_BASE % code
    req.rec_num = str(phone_num)
    req.sms_template_code = settings.ALIDAYU_SMS_TEMPLATE_CODE
    try:
        resp = req.getResponse()
        print(resp)
        cache.set(phone_num, code, timeout=settings.ALIDAYU_CACHE_TIMEOUT)
    except Exception as e:
        logger.error(e)
    else:
        return code


@shared_task
def send_email_captcha(email_addr):
    code = gen_captcha()
    try:
        # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
        send_mail('天天生鲜，邮箱验证',
                  '验证码是：%s' % code,
                  settings.EMAIL_HOST_USER,
                  [email_addr],
                  fail_silently=False)
    except Exception as e:
        logger.error(e)
    else:
        cache.set(email_addr, code, timeout=settings.ALIDAYU_CACHE_TIMEOUT)
        return code
