import scrapy
from scrapy.selector import Selector


class SongAbstract(scrapy.Spider):
    name = 'test'

    def __init__(self):
        self.headers = {
            'Referer': 'http://music.163.com/',
            'Host': 'music.163.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

    def start_requests(self):
        urls = ['http://music.163.com/discover/toplist']

        for url in urls:
            yield scrapy.FormRequest(url=url, method='GET', callback=self.get_list_id)

    def get_list_id(self, response):
        selector = Selector(response)
        # 最后一项是冗余数据需要去掉
        url_list = selector.xpath('//body//a[@class="s-fc0"]/@href')[:-1].extract()
        for url in url_list:
            yield scrapy.FormRequest(url='http://music.163.com/m{}'.format(url), method='GET',
                                     callback=self.parse_song_list, headers=self.headers)

    def parse_song_list(self, response):
        selector = Selector(response)
        titles = selector.xpath('//body//ul[@class="f-hide"]/li/a/text()').extract()
        print(titles)
