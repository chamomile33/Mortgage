import scrapy
from urllib.parse import urlencode
from spider_cian.items import RegionId
import re


API = '0b850001503ff83ce6ac36c5b2a30bd8'

def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload) 
    return proxy_url


class CityparsespiderSpider(scrapy.Spider):
    name = 'CityParseSpider'
    start_urls = ['http://cian.ru/']


    def start_requests(self):
        for location in range(4551, 6941):
            print(location)
            path =  f'https://www.cian.ru/map/?deal_type=sale&engine_version=2&offer_type=flat&region={location}'
            yield scrapy.Request(url=get_url(path), callback=self.parse,cb_kwargs={'id':location})
            
    def parse(self, response,id):
        item = RegionId()
        item['id'] = id
        ret = response.xpath('//script[contains(text(),"window._cianConfig[\'map-search-frontend\']")]/text()').extract()[0]
        config_part = re.findall('(?<=items\":)[^\]]*\]',ret)[0]
        if 'null' in config_part[:10]:
            item['name'] = None
        else:
            tags = eval(config_part)
            item['name'] = tags[-1]['name']
        yield item
