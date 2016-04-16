#!usr/bin/env python
# coding=utf-8
"""
author:wubaichuan

"""
from django import forms
from blog.models import Article, User, UserProfile


class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=30, help_text=u"15字以内的标题")
    article_type_id = forms.ChoiceField(choices=[(1, 'python'), (2, 'javascript'),
                                                 (3, 'away'), (4, 'home')], help_text=u'选择文章类型')
    summary = forms.CharField(max_length=256, help_text=u"请输入概述")
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Article
        fields = ('title', 'article_type_id', 'summary', 'content')


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')



