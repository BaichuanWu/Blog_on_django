# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='news',
            new_name='article',
        ),
        migrations.AlterField(
            model_name='article',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 21, 46, 52, 473895)),
        ),
        migrations.AlterField(
            model_name='article',
            name='revised_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 18, 21, 46, 52, 473922), auto_now=True),
        ),
    ]
