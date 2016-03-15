# coding=utf-8
from django.conf.urls import patterns, url ,include
from django.contrib import admin
from myServer import settings

urlpatterns = patterns("",
    url(r'^admin', include(admin.site.urls)),
    url(r'^', include('appName.app_urls')),
                       )