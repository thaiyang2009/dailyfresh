"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),

    url(r'^register_handle/', views.register_handle, name='register_handle'),
    url(r'^login_handle/', views.login_handle, name='login_handle'),


    url(r'^check_username/$', views.check_username, name='check_username'),
    url(r'^check_email/$', views.check_email, name='check_email'),

    url(r'^site/$', views.site, name='site'),
    url(r'^info/$', views.info, name='info'),
    url(r'^order/$', views.order, name='order'),
    url(r'^area_handle/$', views.area_handle, name='area_handle'),
    url(r'^change_site/(\d+)/$', views.change_site, name='change_site'),
    url(r'^edit_info/$', views.edit_info, name='edit_info'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^send_captcha/$', views.send_captcha, name='send_captcha'),

    url(r'add_address/$', views.add_address, name="add_address"),
]
