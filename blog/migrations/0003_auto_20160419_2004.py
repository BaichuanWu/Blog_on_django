# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20160418_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 20, 4, 39, 408451)),
        ),
        migrations.AlterField(
            model_name='article',
            name='revised_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 20, 4, 39, 408477), auto_now=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 4, 19, 20, 4, 39, 409061)),
        ),
    ]
