import json
from datetime import datetime

import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader

from spider.cloud_spider.items import SongListItem, CommentItem
from spider.cloud_api import api_comment, api_song_url
from spider.database import generate_comment_index


class SongAbstract(scrapy.Spider):
    name = 'song_list'

    def __init__(self, *args, **kwargs):
        super(SongAbstract, self).__init__(*args, **kwargs)
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
            l.add_value('song_name', song_name_list[index])
            l.add_value('type', response.meta['type'])
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


    def parse_comments(self, response):
        l = ItemLoader(item=CommentItem())
        comment_id = response.meta['comment_id']
        json_response = json.loads(response.body_as_unicode())

        hot_comments = [{'name': item['user']['nickname'],
                         'content': item['content'],
                         'stars': item['likedCount'],
                         'replyed_name': item['beReplied'][0]['user']['nickname']
                         if item['beReplied'] else None,
                         'replyed_content': item['beReplied'][0]['content']
                         if item['beReplied'] else None}
                        for item in json_response['hotComments']]
        comments = [{'name': item['user']['nickname'],
                         'content': item['content'],
                         'stars': item['likedCount'],
                         'replyed_name': item['beReplied'][0]['user']['nickname']
                         if item['beReplied'] else None,
                         'replyed_content': item['beReplied'][0]['content']
                         if item['beReplied'] else None}
                        for item in json_response['comments']]

        l.add_value('_id', comment_id)
        l.add_value('hot_comments', hot_comments)
        l.add_value('comments', comments)

        time_now = datetime.now()

        l.add_value('update_time', time_now)
        l.add_value('create_time', time_now)

        yield  l.load_item()

    def get_source_url(self, response):
        loader = response.meta['loader']
        json_response = json.loads(response.body_as_unicode())['data']

        source_url = json_response[0]['url']
        loader.add_value('source_url', source_url)

        time_now = datetime.now()

        loader.add_value('update_time', time_now)
        loader.add_value('create_time', time_now)

        yield loader.load_item()