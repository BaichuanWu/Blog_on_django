#!usr/bin/env python
# coding=utf-8
"""
author:wubaichuan

"""
from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime
from django.contrib.auth.models import User


class ArticleType(models.Model):
    display = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.display)
        super(ArticleType, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.display


class Article(models.Model):
    title = models.CharField(max_length=30, unique=True)
    summary = models.CharField(max_length=256)
    content = models.TextField()
    reply_count = models.IntegerField(default=0)
    author = models.ForeignKey('UserProfile')
    article_type = models.ForeignKey('ArticleType')
    create_date = models.DateTimeField(default=datetime.now())
    revised_date = models.DateTimeField(auto_now=True, default=datetime.now())

    def __unicode__(self):
        return self.title


class Reply(models.Model):
    content = models.TextField()
    user = models.ForeignKey('UserProfile')
    article = models.ForeignKey('Article')
    create_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.content


class Chat(models.Model):
    content = models.TextField()
    user = models.ForeignKey('UserProfile')
    create_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.content


class MessageBoard(models.Model):
    content = models.TextField()
    user = models.ForeignKey('UserProfile')
    create_date = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.content


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username

