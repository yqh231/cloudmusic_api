from spider.cloud_spider.spiders.playlist import PlayLists
import scrapy

class PlayListChinese(PlayLists):
    name = 'play_list_chinese'

    def __init__(self, *args, **kwargs):
        super(PlayListChinese, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = ['http://music.163.com/discover/playlist/?order=hot&cat=华语&limit=35&offset={}'.format(page * 35) for page in range(40)]
        for url in urls:
            yield scrapy.FormRequest(url=url, method='GET', callback=self.get_list_id)