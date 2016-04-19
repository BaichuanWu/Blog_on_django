# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20160419_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favor',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='favor',
            name='target',
        ),
        migrations.DeleteModel(
            name='Favor',
        ),
        migrations.RemoveField(
            model_name='article',
            name='favor_count',
        ),
        migrations.AlterField(
            model_name='article',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 22, 5, 11, 702794)),
        ),
        migrations.AlterField(
            model_name='article',
            name='revised_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 22, 5, 11, 702822), auto_now=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 22, 5, 11, 703399)),
        ),
    ]
