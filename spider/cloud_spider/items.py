# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 这里建立模型
class SongListItem(scrapy.Item):
    _id = scrapy.Field()
    song_name = scrapy.Field()
    type = scrapy.Field()
    source_url = scrapy.Field()
    comment_id = scrapy.Field()
    update_time = scrapy.Field()
    create_time = scrapy.Field()


class CommentItem(scrapy.Item):
    _id = scrapy.Field()
    hot_comments = scrapy.Field()
    comments = scrapy.Field()
    update_time = scrapy.Field()
    create_time = scrapy.Field()
