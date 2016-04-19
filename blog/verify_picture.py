#!usr/bin/env python
# -*-coding:utf-8-*-
"""
author:wubaichuan

"""


def verify(img):
    suffix = ('jpg', 'png', 'gif', 'jpeg')
    if img.size > 1024 or img.name.split('.')[-1].lower() not in suffix:
        return False
