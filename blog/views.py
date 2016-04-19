#!usr/bin/env python
# -*-coding:utf-8-*-

from django.shortcuts import render, redirect, HttpResponse
from models import Article, ArticleType, User, Reply
from forms import ArticleForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# from django.core import serializers
from datetime import datetime
import json
from json_type import CJsonEncoder
from page_tool import PageHelper, page_modify


def index(request, page=1):
    page = page_modify(page)
    article_list = Article.objects.order_by('-create_date')
    count_articles = article_list.count()
    page_help = PageHelper(int(page), count_articles)
    user_list = User.objects.order_by('-date_joined')
    articles = article_list[page_help.start_item:page_help.end_item]
    context_dict = {'articles': articles, 'user_list': user_list}
    context_dict.update(page_help.page_info)
    visits = int(request.session.get('visits', 1))
    response = render(request, 'blog/index.html', context_dict)
    reset_last_visit = False
    if 'last_visit' in request.session:
        last_visit = request.session['last_visit']
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")  # str-->object
        if (datetime.now() - last_visit_time).seconds > 0:
            visits += 1
            reset_last_visit = True
    else:
        reset_last_visit = True
        context_dict['visits'] = visits
        response = render(request, 'blog/index.html', context_dict)
    if reset_last_visit:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    print request.session['last_visit']
    return response


def user_login(request):
    context = {'warn': None}
    if request.method == 'POST':
        print request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                context['warn'] = u'封号中,如有疑问请联系管理员'
                return render(request, 'blog/auth/login.html', context)
        else:
            print u'无效信息:%s,%s' % (username, password)
            context['warn'] = u'错误的账号或密码'
            return render(request, 'blog/auth/login.html', context)
    else:
        return render(request, 'blog/auth/login.html', context)


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                print profile.picture
                print type(profile.picture)
            profile.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/blog/')
        else:
            print user_form.errors
            error = user_form.errors.as_data().values()[0][0].messages[0]
            print type(error)
            return render(request, 'blog/auth/register.html',
                          {'error': error})
    else:
        return render(request, 'blog/auth/register.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/blog/')


def about(request):
    return render(request, 'blog/about.html')


def article_type(request, type_slug):
    context_dict = {}
    print type_slug
    try:
        a_type = ArticleType.objects.get(slug=type_slug)
        context_dict['article_type'] = a_type
        article = Article.objects.filter(article_type=a_type).order_by('-create_date')
        context_dict['articles'] = article
        print context_dict
    except ArticleType.DoesNotExist:
        pass
    return render(request, 'blog/article/atype.html', context_dict)


def article(request, art_id):
    context_dict = {}
    print art_id
    try:
        art = Article.objects.get(id=art_id)
        context_dict['article'] = art
    except ArticleType.DoesNotExist:
        pass
    return render(request, 'blog/article/article.html', context_dict)


def profile(request, author_id):
    context_dict = {}
    print author_id
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
        print reply_list
        return HttpResponse(reply_list)


@login_required
def add_reply(request):
    reply_list = {}
    if request.method == 'POST':
        rid = request.POST.get('nid')
        content = request.POST.get('data')
        print rid, content, request.user.username
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
        print 1
        return HttpResponse(reply_list)


@login_required
def add_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            summary = request.POST.get('summary')
            content = request.POST.get('content')
            type_id = request.POST.get('article_type_id')
            Article.objects.get_or_create(title=title, summary=summary, content=content,
                                          article_type_id=type_id, author_id=request.user.id)

            return redirect('/blog/')
        else:
            print form.errors
            error = form.errors.as_data().values()[0][0].messages[0]
            print type(error)
            return render(request, 'blog/article/add_article.html',
                          {'error': error})
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







