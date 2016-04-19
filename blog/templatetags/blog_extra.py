#!usr/bin/env python
# -*-coding:utf-8-*-
"""
author:wubaichuan

"""

from django import template
from blog.models import User

register = template.Library()


@register.inclusion_tag('blog/plug_in/_new_reg.html')
def new_reg():
    return {'user_list': User.objects.all().order_by('-last_login')[0:8]}


