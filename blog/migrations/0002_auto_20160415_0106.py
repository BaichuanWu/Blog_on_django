# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='slug',
        ),
        migrations.AlterField(
            model_name='article',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 15, 1, 6, 33, 330685)),
        ),
        migrations.AlterField(
            model_name='article',
            name='revised_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 15, 1, 6, 33, 330708), auto_now=True),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 15, 1, 6, 33, 329507)),
        ),
    ]
