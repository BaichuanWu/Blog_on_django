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


def populate():
    python_cat = add_type('Python')

    add_article(cat=python_cat,
                title=u"python333",
                summary=u"在实际工作中，对于小数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    add_article(cat=python_cat,
                title=u"python332",
                summary=u"在实际工作中，对于小11数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    add_article(cat=python_cat,
                title=u"python99",
                summary=u"在实际工作中，对于小22数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    js_cat = add_type('Javascript')

    add_article(cat=js_cat,
                title=u"javascript2",
                summary=u"在实际工作中，1对于小数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    add_article(cat=js_cat,
                title=u"javascript5",
                summary=u"在实际工作中，1对于小数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    add_article(cat=js_cat,
                title=u"javascript7",
                summary=u"在实际工作中，1对于小数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    away_cat = add_type('Away')

    add_article(cat=away_cat,
                title=u"在家49",
                summary=u"在实际工作中，1对于小数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    add_article(cat=away_cat,
                title=u"在家30",
                summary=u"在实际工作中，1对于小数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    home_cat = add_type('Home')

    add_article(cat=home_cat,
                title=u"在外29",
                summary=u"在实际工作中，1对于小数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    add_article(cat=home_cat,
                title=u"在外19",
                summary=u"在实际工作中，1对于小数据集的简单分析来说，\n"
                        u"使用Excel绝对是最佳选择。但当我们需要更多复杂的统计分析和数据处理时"
                )

    for c in ArticleType.objects.all():
        for p in Article.objects.filter(article_type=c):
            print "- {0} - {1}".format(str(c), str(p))


def add_article(cat, title, summary, content=u'等待补充', use_id=2):
    article = Article.objects.get_or_create(article_type=cat, title=title, summary=summary,
                                            content=content, author_id=use_id)[0]
    return article


def add_type(display):
    a_type = ArticleType.objects.get_or_create(display=display)[0]
    return a_type


if __name__ == '__main__':
    print "Starting blog population script..."
    populate()
