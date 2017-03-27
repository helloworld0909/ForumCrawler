# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


# TODO dynamic item class
class BoardItem(Item):
    board_url = Field()
    board_name = Field()
    pages = Field()
    category = 'board'


class PostItem(Item):
    post_url = Field()
    post_name = Field()
    board_url = Field()
    board_name = Field()
    user_url = Field()
    user_name = Field()
    replies = Field()
    pv = Field()
    date_time = Field()
    content = Field()
    context = Field()
    category = 'post'


class UserItem(Item):
    uid = Field()
    user_url = Field()
    user_name = Field()
    profile = Field()

    category = 'user'


class OfferItem(Item):
    url = Field()
    offer_type = Field()
    uid = Field()

    school = Field()
    degree = Field()
    major = Field()
    result = Field()
    enroll_year = Field()
    enroll_semester = Field()
    notice_time = Field()

    toefl = Field()
    ielts = Field()
    gre = Field()
    sub = Field()
    gmat = Field()
    undergraduate_gpa = Field()
    undergraduate_school = Field()
    undergraduate_major = Field()
    master_gpa = Field()
    master_school = Field()
    master_major = Field()
    other_info = Field()

    category = 'offer'
