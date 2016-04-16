# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=30)),
                ('summary', models.CharField(max_length=256)),
                ('content', models.TextField()),
                ('favor_count', models.IntegerField(default=0)),
                ('reply_count', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(default=datetime.datetime(2016, 4, 16, 21, 30, 32, 789743))),
                ('revised_date', models.DateTimeField(default=datetime.datetime(2016, 4, 16, 21, 30, 32, 789774), auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display', models.CharField(unique=True, max_length=50)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MessageBord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('news', models.ForeignKey(to='blog.Article')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(to='blog.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='messagebord',
            name='user',
            field=models.ForeignKey(to='blog.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(to='blog.UserProfile'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='article_type',
            field=models.ForeignKey(to='blog.ArticleType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(to='blog.UserProfile'),
            preserve_default=True,
        ),
    ]
