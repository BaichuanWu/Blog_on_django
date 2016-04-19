#!usr/bin/env python
# -*-coding:utf-8-*-
"""
author:wubaichuan

"""
import random
import string
from threading import Thread
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_email(title, content, to):
    msg = EmailMultiAlternatives(title, content, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(content, 'text/html')
    msg.send()


# def send_async_email(title, content, to):
#     thr = Thread(target=send_email, args=[title, content, title])
#     thr.start()
#     return thr

def psw_generate():
    psw = ''
    num = random.randint(8, 13)
    for i in range(num):
        psw += random.choice(string.letters)
    return psw
