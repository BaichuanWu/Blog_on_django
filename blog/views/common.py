#!usr/bin/env python
# -*-coding:utf-8-*-
"""
author:wubaichuan

"""
import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from blog.models import Article, MessageBoard
from blog.tools.page_tool import PageHelper, page_modify
from blog.tools.json_type import CJsonEncoder


def index(request, page=1):
    page = page_modify(page)
    article_list = Article.objects.order_by('-create_date')
    count_articles = article_list.count()
    page_help = PageHelper(page, count_articles)
    articles = article_list[page_help.start_item:page_help.end_item]
    context_dict = {'articles': articles}
    context_dict.update(page_help.page_info)
    if request.session.get('notice', None):
        context_dict.update({'notice': request.session['notice']})
        print context_dict
        request.session['notice'] = None
    response = render(request, 'blog/index.html', context_dict)
    return response


def about(request):
    return render(request, 'blog/about.html')


def message_board(request, page=1):
    page = page_modify(page)
    message_list = MessageBoard.objects.all().order_by('create_date')
    count_message = message_list.count()
    page_help = PageHelper(page, count_message, 10)
    message = message_list[page_help.start_item:page_help.end_item]
    context_dict = {'messages': message, 'in_url': 'message_board/'}
    context_dict.update(page_help.page_info)
    return render(request, 'blog/message_board.html', context_dict)


@login_required
def add_message(request):
    reply_list = {}
    if request.method == 'POST':
        content = request.POST.get('data')
        try:
            new_r = MessageBoard.objects.create(content=content,
                                                user = request.user.userprofile)
            reply_list = {'content': new_r.content, 'create_date': new_r.create_date,
                          'user': new_r.user.user.username, 'id': new_r.user.id}
            reply_list = json.dumps(reply_list, cls=CJsonEncoder)
        except Exception, e:
            print e
        return HttpResponse(reply_list)




# @login_required
# def add_chat(request):
#     reply_list = {}
#     if request.method == 'POST':
#         rid = request.POST.get('nid')
#         content = request.POST.get('data')
#         print rid, content, request.user.username
#         try:
#             new_r = Reply.objects.create(content=content,
#                                          article_id=rid,
#                                          user=request.user.userprofile,
#                                          )
#             art = Article.objects.get(id=rid)
#             art.reply_count = Reply.objects.filter(article_id=rid).count()
#             art.save()
#             reply_list = {'content': new_r.content, 'create_date': new_r.create_date,
#                           'user': new_r.user.user.username, 'count': art.reply_count
#                           }
#             reply_list = json.dumps(reply_list, cls=CJsonEncoder)
#         except Exception, e:
#             print e
#         print 1
#         return HttpResponse(reply_list)
