#!usr/bin/env python
# coding=utf-8
"""
author:wubaichuan

"""
from django import forms
from blog.models import Article, User, UserProfile


error_messages = {
    'username': {
        'required': u'必须填写用户名',
        'min_length': u'用户名长度过短（3-12个字符）',
        'max_length': u'用户名长度过长（3-12个字符）',
        'invalid': u'用户名格式错误'
    },
    'email': {
        'required': u'必须填写E-mail',
        'invalid': u'Email地址无效'
    },
    'password': {
        'required': u'必须填写密码',
        'min_length': u'密码长度过短（6-12个字符）',
        'max_length': u'密码名长度过长（6-12个字符）',
    },
    'title': {
        'required': u'必须填写标题',
        'invalid': u'标题格式错误'
    },
    'summary': {
        'required': u'必须填写简介',
        'invalid': u'简介格式错误'
    },
    'content': {
        'required': u'必须填写内容',
        'invalid': u'内容格式错误'
    },
}


class ArticleForm(forms.ModelForm):
    title = forms.CharField(max_length=30, help_text=u"15字以内的标题",
                            error_messages=error_messages.get('title'))
    article_type_id = forms.ChoiceField(choices=[(1, 'python'), (2, 'javascript'),
                                                 (3, 'away'), (4, 'home')], help_text=u'选择文章类型')
    summary = forms.CharField(max_length=256, help_text=u"请输入概述",
                              error_messages=error_messages.get('summary'))
    content = forms.CharField(widget=forms.Textarea, error_messages=error_messages.get('content'))

    class Meta:
        model = Article
        fields = ('title', 'article_type_id', 'summary', 'content')

    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            Article.objects.get(title=title)
            raise forms.ValidationError(u'文章标题已使用')
        except Article.DoesNotExist:
            return title


class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=12, min_length=3, error_messages=error_messages.get('username'))
    email = forms.EmailField(error_messages=error_messages.get('email'))
    password = forms.CharField(widget=forms.PasswordInput(), max_length=12,
                               min_length=6, error_messages=error_messages.get('password'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            raise forms.ValidationError(u'用户名已被注册')
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(u'邮箱已被注册')
        except User.DoesNotExist:
            return email


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')





