#!usr/bin/env python
# coding=utf-8
"""
author:wubaichuan

"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblogshare.settings')

import django

django.setup()

from blog.models import Article, ArticleType

python_this = """
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
"""

js_this = u"""
JavaScript一种直译式脚本语言，是一种动态类型、弱类型、基于原型的语言，
内置支持类型。它的解释器被称为JavaScript引擎，为浏览器的一部分，广泛用于
客户端的脚本语言，最早是在HTML（标准通用标记语言下的一个应用）网页上使用
，用来给HTML网页增加动态功能。在1995年时，由Netscape公司的Brendan Eich
，在网景导航者浏览器上首次设计实现而成。因为Netscape与Sun合作，Netscape管
理层希望它外观看起来像Java，因此取名为JavaScript。但实际上它的语法风格与Sel
f及Scheme较为接近.为了取得技术优势，微软推出了JScript，CEnvi推出ScriptEase，
与JavaScript同样可在浏览器上运行。为了统一规格，因为JavaScript兼容于ECMA标准，
因此也称为ECMAScript。
"""

away_this = """
Stray birds of summer come to my window to sing and fly away.
And yellow leaves of autumn, which have no songs, flutter and fall
there with a sign.
"""

home_this = """
The fish in the water is silent, the animal on the earth is noisy,
the bird in the air is singing.
But Man has in him the silence of the sea, the noise of the earth and
the music of the air.
"""


def populate(num):
    python_cat = add_type('Python')

    add_article(cat=python_cat,
                title=u"测试标题python-%s" % num,
                summary=(u"测试简介python-%s" % num) * 5,
                content=python_this
                )

    js_cat = add_type('Javascript')

    add_article(cat=js_cat,
                title=u"测试标题javascript-%s" % num,
                summary=(u"测试简介javascript-%s" % num) * 5,
                content=js_this
                )

    away_cat = add_type('Away')

    add_article(cat=away_cat,
                title=u"测试标题away-%s" % num,
                summary=(u"测试简介away-%s" % num) * 5,
                content=away_this
                )

    home_cat = add_type('Home')

    add_article(cat=home_cat,
                title=u"测试标题home-%s" % num,
                summary=(u"测试简介home-%s" % num) * 5,
                content=home_this
                )

    for c in ArticleType.objects.all():
        for p in Article.objects.filter(article_type=c):
            print "- {0} - {1}".format(str(c), str(p))


def add_article(cat, title, summary, content, use_id=1):
    article = Article.objects.get_or_create(article_type=cat, title=title, summary=summary,
                                            content=content, author_id=use_id)[0]
    return article


def add_type(display):
    a_type = ArticleType.objects.get_or_create(display=display)[0]
    return a_type


if __name__ == '__main__':
    print "Starting blog population script..."
    for i in range(2, 30):
        populate(i)

