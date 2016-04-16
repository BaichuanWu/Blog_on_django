#!usr/bin/env python
# -*-coding:utf-8-*-

from django.shortcuts import render, redirect
from models import UserInfo, UserType, Article, ArticleType
from forms import ArticleForm


# Create your views here.


def index(request):
    article_list = Article.objects.order_by('-revised_date')
    context_dict = {'articles': article_list}
    return render(request, 'blog/index.html', context_dict)


def login(request):
    """
    send an email
    """
    if request.method == 'POST':
        pass
    return render(request, 'blog/login.html')


def register(request):
    """
    AJAX
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        print email
        try:
            UserInfo.objects.create(username=username, password=password, email=email, user_type_id=3)
        except Exception, e:
            print e
            return render(request, 'blog/register.html')
        return redirect('/blog/index/')
    return render(request, 'blog/register.html')


def logout(request):
    """
    delete session

    """
    pass


def about(request):
    return render(request, 'blog/about.html')


def article_type(request, type_slug):
    context_dict = {}
    print type_slug
    try:
        a_type = ArticleType.objects.get(slug=type_slug)
        context_dict['article_type'] = a_type
        article = Article.objects.filter(article_type=a_type).order_by('-revised_date')
        context_dict['articles'] = article
        print context_dict
    except ArticleType.DoesNotExist:
        pass
    return render(request, 'blog/atype.html', context_dict)


def article(request, art_id):
    context_dict = {}
    print art_id
    try:
        art = Article.objects.get(id=art_id)
        context_dict['article'] = art
    except ArticleType.DoesNotExist:
        pass
    return render(request, 'blog/article.html', context_dict)


def add_article(request):
    """
    ADD CACHE

    """
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            print request.POST
            title = request.POST.get('title')
            summary = request.POST.get('summary')
            content = request.POST.get('content')
            type_id = request.POST.get('article_type_id')
            Article.objects.get_or_create(title=title, summary=summary, content=content,
                                          article_type_id=type_id, user_id=1)

            return redirect('/blog/index/')
        else:
            print form.errors
    else:
        form = ArticleForm()
        print form.visible_fields()
    return render(request, 'blog/add_article.html', {'form': form})
