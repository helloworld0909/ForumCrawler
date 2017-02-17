# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class BoardItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    name = Field()
    pages = Field()
    category = 'board'


class PostItem(Item):
    url = Field()
    name = Field()
    author_url = Field()
    author_name = Field()
    replies = Field()
    pv = Field()
    date_time = Field()
    content = Field()
    category = 'post'


class UserItem(Item):

    category = 'user'
