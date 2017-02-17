# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class ForumItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = Field()
    name = Field()
    pages = Field()
    category = 'forum'


class PostItem(Item):

    category = 'post'


class UserItem(Item):

    category = 'user'
