# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20160419_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageBoard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField(default=datetime.datetime(2016, 4, 21, 22, 42, 48, 752836))),
                ('user', models.ForeignKey(to='blog.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='messagebord',
            name='user',
        ),
        migrations.DeleteModel(
            name='MessageBord',
        ),
        migrations.AlterField(
            model_name='article',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 22, 42, 48, 751060)),
        ),
        migrations.AlterField(
            model_name='article',
            name='revised_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 22, 42, 48, 751087), auto_now=True),
        ),
        migrations.AlterField(
            model_name='chat',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 22, 42, 48, 752269)),
        ),
        migrations.AlterField(
            model_name='reply',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 21, 22, 42, 48, 751658)),
        ),
    ]
