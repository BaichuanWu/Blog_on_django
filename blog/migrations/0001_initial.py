# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
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
                ('create_date', models.DateTimeField(default=datetime.datetime(2016, 4, 15, 0, 43, 25, 456390))),
                ('revised_date', models.DateTimeField(default=datetime.datetime(2016, 4, 15, 0, 43, 25, 456417), auto_now=True)),
                ('slug', models.SlugField(unique=True)),
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
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('password', models.CharField(max_length=256)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('create_date', models.DateTimeField(default=datetime.datetime(2016, 4, 15, 0, 43, 25, 454887))),
                ('last_date', models.DateTimeField(default=b'2016-4-10')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('display', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_type',
            field=models.ForeignKey(to='blog.UserType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reply',
            name='user',
            field=models.ForeignKey(to='blog.UserInfo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='messagebord',
            name='user',
            field=models.ForeignKey(to='blog.UserInfo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(to='blog.UserInfo'),
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
            field=models.ForeignKey(to='blog.UserInfo'),
            preserve_default=True,
        ),
    ]
