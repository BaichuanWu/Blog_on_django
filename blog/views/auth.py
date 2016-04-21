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
from blog.forms import UserForm, UserProfileForm
from blog.models import User
from blog.tools.email_tool import send_email, psw_generate


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
            new_psw = request.POST.get('password')
            print new_psw
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

