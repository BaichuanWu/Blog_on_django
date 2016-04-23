#!usr/bin/env python
# -*-coding:utf-8-*-
"""
author:wubaichuan

"""


class PageHelper(object):
    def __init__(self, current_page, items, per_page=4):
        self.current_page = current_page
        self.items = items
        self.per_page = per_page

    @property
    def all_page(self):
        temp = divmod(self.items, self.per_page)
        if self.items == 0:
            count = 1
        elif temp[1] == 0:
            count = temp[0]
        else:
            count = temp[0] + 1
        return count

    @property
    def start_page(self):
        if self.current_page <= 5:
            start = 1
        else:
            start = self.current_page - 4
        return start

    @property
    def end_page(self):
        if self.all_page - self.current_page <= 4:
            end = self.all_page
        else:
            end = self.current_page + 4
        return end

    @property
    def start_item(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end_item(self):
        return self.start_item + self.per_page

    @property
    def previous(self):
        if self.current_page == 1:
            pre = None
        else:
            pre = self.current_page - 1
        return pre

    @property
    def after(self):
        if self.current_page == self.end_page:
            after = None
        else:
            after = self.current_page + 1
        return after

    @property
    def page_info(self):
        return {'page_list': range(self.start_page, self.end_page + 1), 'all_page': self.all_page,
                'current_page': self.current_page, 'previous_page': self.previous, 'next_page': self.after}


def page_modify(page):
    if page == '':
        page = 1
    else:
        page = int(page)
    return page
