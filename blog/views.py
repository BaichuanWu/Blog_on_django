#!usr/bin/env python
# -*-coding:utf-8-*-

from django.shortcuts import render, redirect
from models import Article, ArticleType
from forms import ArticleForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    article_list = Article.objects.order_by('-revised_date')
    context_dict = {'articles': article_list}
    return render(request, 'blog/index.html', context_dict)


def user_login(request):
    """
    send an email
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                return HttpResponse(u'封号中,如有疑问请联系管理员')
        else:
            print u'无效信息:%s,%s' % (username, password)
            return HttpResponse(u'无效的用户名或密码')
    else:
        return render(request, 'blog/login.html')


def register(request):
    """
    AJAX
    """
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     email = request.POST.get('email')
    #     print email
    #     try:
    #         UserInfo.objects.create(username=username, password=password, email=email, user_type_id=3)
    #     except Exception, e:
    #         print e
    #         return render(request, 'blog/register.html')
    #     return redirect('/blog/index/')
    # return render(request, 'blog/register.html')
    registered = False
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
            profile.save()
            registered = True
            # return redirect('/blog/index/')
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'blog/register.html',
                  {'user_form': user_form, 'profile_form': profile_form,
                   'registered': registered})


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


@login_required
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

            return redirect('/blog/')
        else:
            print form.errors
    else:
        form = ArticleForm()
        print form.visible_fields()
    return render(request, 'blog/add_article.html', {'form': form})
