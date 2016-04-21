#!usr/bin/env python
# -*-coding:utf-8-*-
"""
author:wubaichuan

"""
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from blog.forms import ArticleForm
from blog.models import Article, ArticleType, User, Reply
from blog.tools.json_type import CJsonEncoder


def article_type(request, type_slug):
    context_dict = {}
    try:
        a_type = ArticleType.objects.get(slug=type_slug)
        context_dict['article_type'] = a_type
        arts = Article.objects.filter(article_type=a_type).order_by('-create_date')
        context_dict['articles'] = arts
        print context_dict
    except ArticleType.DoesNotExist:
        pass
    return render(request, 'blog/article/atype.html', context_dict)


def article(request, art_id):
    context_dict = {}
    try:
        art = Article.objects.get(id=art_id)
        context_dict['article'] = art
    except ArticleType.DoesNotExist:
        pass
    return render(request, 'blog/article/article.html', context_dict)


def profile(request, author_id):
    context_dict = {}
    try:
        user = User.objects.get(id=author_id)
        context_dict['author'] = user
        article_list = Article.objects.filter(author_id=author_id).order_by('-revised_date')
        context_dict['articles'] = article_list
    except ArticleType.DoesNotExist:
        pass
    return render(request, 'blog/article/profile.html', context_dict)


def get_reply(request):
    if request.method == 'POST':
        rid = request.POST.get('nid')
        reply_list = Reply.objects.filter(article_id=rid).values('id', 'content',
                                                                 'create_date',
                                                                 'user__user__username').order_by('create_date')
        reply_list = list(reply_list)
        reply_list = json.dumps(reply_list, cls=CJsonEncoder)
        return HttpResponse(reply_list)


@login_required
def add_reply(request):
    reply_list = {}
    if request.method == 'POST':
        rid = request.POST.get('nid')
        content = request.POST.get('data')
        try:
            new_r = Reply.objects.create(content=content,
                                         article_id=rid,
                                         user=request.user.userprofile,
                                         )
            art = Article.objects.get(id=rid)
            art.reply_count = Reply.objects.filter(article_id=rid).count()
            art.save()
            reply_list = {'content': new_r.content, 'create_date': new_r.create_date,
                          'user': new_r.user.user.username, 'count': art.reply_count
                          }
            reply_list = json.dumps(reply_list, cls=CJsonEncoder)
        except Exception, e:
            print e
        return HttpResponse(reply_list)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        title = request.POST.get('title')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        type_id = request.POST.get('article_type_id')
        if form.is_valid():

            Article.objects.get_or_create(title=title, summary=summary, content=content,
                                          article_type_id=type_id, author_id=request.user.id)
            request.session['notice'] = u'%s发布成功' % title
            return redirect('/blog/')
        else:
            print form.errors
            error = form.errors.as_data().values()[0][0].messages[0]
            return render(request, 'blog/article/add_article.html',
                          {'error': error, 'title': title, 'summary': summary,
                           'content': content})
    else:
        return render(request, 'blog/article/add_article.html')


@login_required
def delete_article(request, art_id):
    art_id = int(art_id)
    art = Article.objects.filter(id=art_id)[0]
    if request.user.id == art.author.user.id:
        art.delete()
        return redirect('/blog/profile/%d' % request.user.id)
    else:
        return redirect('/blog/')


@login_required
def edit_article(request, art_id):
    art_id = int(art_id)
    art = Article.objects.filter(id=art_id)[0]
    if request.method == 'POST':
        content = request.POST.get('content')
        if content == '':
            return render(request, 'blog/article/edit_article.html',
                          {'error': u'必须填写内容', 'article': art})
        art.content = content
        art.save()
        return redirect('/blog/profile/%d' % request.user.id)
    else:
        return render(request, 'blog/article/edit_article.html', {'article': art})
