from spider.cloud_spider.spiders.song import SongAbstract
import json
from datetime import datetime

import scrapy
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

from spider.cloud_spider.items import SongListItem, PlayListItem, CommentItem
from spider.cloud_api import api_comment, api_song_url
from spider.database import generate_comment_index


class PlayLists(SongAbstract):
    name = 'play_list_japanese'

    def __init__(self, *args, **kwargs):
        super(PlayLists, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = ['http://music.163.com/discover/playlist/?order=hot&cat=日语&limit=35&offset={}'.format(page * 35) for page in range(40)]
        for url in urls:
            yield scrapy.FormRequest(url=url, method='GET', callback=self.get_list_id)

    def get_list_id(self, response):
        selector = Selector(response)
        # 最后一项是冗余数据需要去掉

        url_list = selector.xpath('//body//p[@class="dec"]/a/@href').extract()

        for url in url_list:

            yield scrapy.FormRequest(url='http://music.163.com/m{}'.format(url), method='GET',
                                     callback=self.parse_song_list, headers=self.headers)

    def parse_song_list(self, response):
        selector = Selector(response)

        song_name_list = selector.xpath('//body//ul[@class="f-hide"]/li/a/text()').extract()
        song_id_list = selector.xpath('//body//ul[@class="f-hide"]/li/a/@href').extract()
        title = selector.xpath('//title/text()').extract()
        for index, id_ in enumerate(song_id_list):
            l = ItemLoader(item=PlayListItem())
            l.add_value('song_name', song_name_list[index])
            l.add_value('title', title)
            yield scrapy.FormRequest(url=self.BASE_URL + id_, meta={'song_id': id_[9:], 'loader': l}, method='GET',
                                     headers=self.headers, callback=self.parse_single_song)

    def parse_single_song(self, response):
        loader = response.meta['loader']
        selector = Selector(response)
        singer = selector.xpath('//title/text()').extract()
        loader.add_value('singer', singer)
        loader.add_value('_id', response.meta['song_id'])

        comment_data, comment_url = api_comment(response.meta['song_id'], 0, 100)
        source_data, source_url = api_song_url(response.meta['song_id'])
        comment_id = generate_comment_index()['comment_index']
        loader.add_value('comment_id', comment_id)

        yield scrapy.FormRequest(url=comment_url, method='POST', headers=self.headers,
                                 formdata=comment_data, callback=self.parse_comments,
                                 meta={'comment_id': comment_id})

        yield scrapy.FormRequest(url=source_url, method='POST', headers=self.headers,
                                 formdata=source_data, meta={'loader': loader}, callback=self.get_source_url)



