import json

import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader

from spider.cloud_spider.items import SongListItem, CommentItem
from spider.cloud_api import api_comment, api_song_url
from spider.database import generate_comment_index


class SongAbstract(scrapy.Spider):
    name = 'test'

    def __init__(self):
        self.headers = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

        self.BASE_URL = 'http://music.163.com'

    def start_requests(self):
        urls = ['http://music.163.com/discover/toplist']

        for url in urls:
            yield scrapy.FormRequest(url=url, method='GET', callback=self.get_list_id)

    def get_list_id(self, response):
        selector = Selector(response)
        # 最后一项是冗余数据需要去掉

        url_list = selector.xpath('//body//a[@class="s-fc0"]/@href')[:-1].extract()
        type_ = 0
        for url in url_list:
            type_ += 1
            yield scrapy.FormRequest(url='http://music.163.com/m{}'.format(url), method='GET',
                                     callback=self.parse_song_list, headers=self.headers, meta={'type': type_})

    def parse_song_list(self, response):
        selector = Selector(response)
        song_name_list = selector.xpath('//body//ul[@class="f-hide"]/li/a/text()').extract()
        song_id_list = selector.xpath('//body//ul[@class="f-hide"]/li/a/@href').extract()

        for index, id_ in enumerate(song_id_list):
            l = ItemLoader(item=SongListItem())
            l.add_value('name', song_name_list[index])
            l.add_value('type', response.meta['type'])
            yield scrapy.FormRequest(url=self.BASE_URL + id_, meta={'song_id': id_[9:], 'loader':l}, method='GET',
                                     headers=self.headers, callback=self.parse_single_song)

    def parse_single_song(self, response):
        loader = response.meta['loader']
        selector = Selector(response)
        singer = selector.xpath('/title/text()')
        loader.add_value('singer', singer)
        comment_data, comment_url = api_comment(response.meta['song_id'], 0, 100)
        comment_id = generate_comment_index()
        loader.add_value('comment_id', comment_id)

        yield scrapy.FormRequest(url=comment_url, method='POST', headers=self.headers,
                                   formdata=comment_data, callback=self.parse_comments, meta={'comment_id':comment_id})



    def parse_comments(self, response):
        comment_id = response.meta['comment_id']
        json_response = json.loads(response.body_as_unicode())
