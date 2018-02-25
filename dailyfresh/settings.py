# coding:utf-8
"""
Django settings for dailyfresh project.

Generated by 'django-admin startproject' using Django 1.9.13.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8wgp)cgx0&!uvfc80#ct-y4y@*0x*%o0^b)ji0)iv#s&s6&9)4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'df_user',
    'df_goods',
    'tinymce',
    'df_cart',
    'df_order',
    'haystack',
    'djcelery',
    # 'django_celery_beat',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dailyfresh.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dailyfresh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 静态文件目录
MEDIA_ROOT = os.path.join(BASE_DIR, 'static')

# 富文本框 admin 配置
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'width': 600,
    'height': 400,
}

TIME_FORMAT = "Y-m-d H:i:s"

# 全文检索配置
# 搜索引擎
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}
#自动生成索引
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 阿里大鱼 短信配置
ALIDAYU_KEY_ID= '24456101'
ALIDAYU_KEY_SECRET = 'ad3f178d008cca744b964110c74a3572'
ALIDAYU_SMS_FREE_SIGN_NAME = "Python论坛"
ALIDAYU_SMS_PARAM_BASE = "{code:'%s'}"
ALIDAYU_SMS_TEMPLATE_CODE = "SMS_71356017"
ALIDAYU_EXTEND = ""
ALIDAYU_SMS_TYPE = "normal"
ALIDAYU_CACHE_TIMEOUT = 60



# 缓存配置，未指定数据则使用数据库1
CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "localhost:6379",
        'TIMEOUT': 60,
    },
}

# 发送邮件配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  #email后端
EMAIL_USE_TLS = False   #是否使用TLS安全传输协议
EMAIL_USE_SSL = True    #是否使用SSL加密，qq企业邮箱要求使用
EMAIL_HOST = 'smtp.qq.com'   #发送邮件的邮箱 的 SMTP服务器，这里用了qq企业邮箱
EMAIL_PORT = 465     #发件箱的SMTP服务器端口
EMAIL_HOST_USER = '515229443@qq.com'    #发送邮件的邮箱地址
EMAIL_HOST_PASSWORD = 'miirbdpzgasxbiga'         #发送邮件的邮箱密码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# celery 配置
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERYD_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'celery', '%n%i.log')
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'celery', 'beat.log')

import djcelery
djcelery.setup_loader()
CELERY_IMPORTS = ('df_user.task')