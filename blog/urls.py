#!usr/bin/env python
# coding=utf-8
"""
author:wubaichuan

"""

from django.conf.urls import patterns, url

urlpatterns = patterns('blog',
                       url(r'^(?P<page>\d*)$', 'views.common.index', name='index'),
                       url(r'^login/$', 'views.auth.user_login', name='user_login'),
                       url(r'^logout/$', 'views.auth.user_logout', name='user_logout'),
                       url(r'^about/$', 'views.common.about', name='about'),
                       url(r'^register/$', 'views.auth.register', name='register'),
                       url(r'^confirm/$', 'views.auth.confirm', name='confirm'),
                       url(r'^reset_psw/$', 'views.auth.reset_psw', name='reset_psw'),
                       url(r'^forgot_psw/$', 'views.auth.forgot_psw', name='forgot_psw'),
                       url(r'^atype/(?P<type_slug>[\w\-]+)/$', 'views.article.article_type', name='article_type'),
                       url(r'^article/(?P<art_id>\d+)/$', 'views.article.article', name='article'),
                       url(r'^add_article/$', 'views.article.add_article', name='add_article'),
                       url(r'^profile/(?P<author_id>\d+)/$', 'views.article.profile', name='profile'),
                       url(r'^getreply/$', 'views.article.get_reply', name='get_reply'),
                       url(r'^addreply/$', 'views.article.add_reply', name='add_reply'),
                       url(r'^delete_article/(?P<art_id>\d+)/$', 'views.article.delete_article', name='delete_article'),
                       url(r'^edit_article/(?P<art_id>\d+)/$', 'views.article.edit_article', name='edit_article'),
                       url(r'^message_board/(?P<page>\d*)$', 'views.common.message_board', name='message_board'),
                       url(r'^add_message/$', 'views.common.add_message', name='add_message'),
                       )
