#!usr/bin/env python
# coding=utf-8
"""
author:wubaichuan

"""
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from django.template import loader, Context
from forms import ArticleForm, UserForm, UserProfileForm
from models import Article, ArticleType, User, Reply, MessageBord
from blog.tools.json_type import CJsonEncoder
from blog.tools.page_tool import PageHelper, page_modify
from blog.tools.email_tool import send_email, psw_generate


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
            prof = profile_form.save(commit=False)
            prof.user = user
            if 'picture' in request.FILES:
                prof.picture = request.FILES['picture']
                print prof.picture
                print type(prof.picture)
            prof.save()
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            request.session['notice'] = u'注册成功*%s*' % username
            return redirect('/blog/')
        else:
            print user_form.errors
            error = user_form.errors.as_data().values()[0][0].messages[0]
            print type(error)
            return render(request, 'blog/auth/register.html',
                          {'error': error})
    else:
        return render(request, 'blog/auth/register.html')


def confirm(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('nid')
        print name
        user = User.objects.filter(username=name)
        if user:
            context['name'] = 0
        else:
            context['name'] = 1
        print 222
        return HttpResponse(json.dumps(context))


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/blog/')


@login_required()
def reset_psw(request):
    context = {}
    if request.method == 'POST':
        username = request.user.username
        old_psw = request.POST.get('old_psw')
        user = authenticate(username=username, password=old_psw)
        if user:
            new_psw = request.POST.get('password1')
            user.set_password(new_psw)
            user.save()
            login(request, user)
            request.session['notice'] = u'密码修改成功'
            return redirect('/blog/')
        else:
            context['warn'] = u'错误旧密码'
            return render(request, 'blog/auth/reset_psw.html', context)
    else:
        return render(request, 'blog/auth/reset_psw.html')


def forgot_psw(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        user = User.objects.filter(email=email, username=username)[0]
        if user:
            new_psw = psw_generate()
            user.set_password(new_psw)
            user.save()
            title = u'*一个博客*找回密码'
            print new_psw
            information = {'email': user.email, 'new_psw': new_psw}
            content = loader.get_template('blog/auth/email_psw.html').render(Context(information))
            send_email(title, content, user.email)
            return render(request, 'blog/auth/forgot_psw.html',
                          {'notice': u'一封邮件已发往%s,请注意查收' % email})
        else:
            return render(request, 'blog/auth/forgot_psw.html',
                          {'notice': u'错误的用户名或邮箱'})
    return render(request, 'blog/auth/forgot_psw.html')


def about(request):
    return render(request, 'blog/about.html')


def article_type(request, type_slug):
    context_dict = {}
    print type_slug
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
            print type(error)
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


def message_bord(request):
    message = MessageBord.objects.all().order_by('-create_date')
    context = {'message': message}
    return render(request, 'blog/message_bord.html', context)
