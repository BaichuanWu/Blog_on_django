#!usr/bin/env python
# coding=utf-8
"""
author:wubaichuan

"""


from django.conf.urls import patterns, url

urlpatterns = patterns('blog',
                       url(r'^index/$', 'views.index', name='index'),
                       url(r'^login/$', 'views.login', name='login'),
                       url(r'^about/$', 'views.about', name='about'),
                       url(r'^register/$', 'views.register', name='register'),
                       url(r'^atype/(?P<type_slug>[\w\-]+)/$', 'views.article_type', name='article_type'),
                       url(r'^article/(?P<art_id>[\d\-]+)/$', 'views.article', name='article'),
                       url(r'^add-article/$', 'views.add_article', name='add_article')
)


