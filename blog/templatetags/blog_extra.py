#!usr/bin/env python
# -*-coding:utf-8-*-
"""
author:wubaichuan

"""

from django import template
from blog.models import User

<<<<<<< HEAD
register = template.Library()


@register.inclusion_tag('blog/plug_in/_new_reg.html')
def new_reg():
    return {'user_list': User.objects.all().order_by('-last_login')[0:8]}

=======
>>>>>>> 98adf8242f75a50d948056c25c0a6dc59ffc2b33

