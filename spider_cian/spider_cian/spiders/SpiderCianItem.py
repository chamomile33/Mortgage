import scrapy
from urllib.parse import urlencode
from spider_cian.items import SpiderCianItem
import re
import pandas as pd
from fuzzywuzzy import process
from fuzzywuzzy import fuzz

API = 'c0069beb54f055d1b2629da27d9f3a12'

def get_url(url):
    payload = {'api_key': API, 'url': url}
    proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload) 
    return proxy_url

class SpidercianitemSpider(scrapy.Spider):
    name = 'SpiderCianItem'
    start_urls = ['http://cian.ru/']

    def __init__(self,url):
        self.url = url
        

    def start_requests(self):
        yield scrapy.Request(url=get_url(self.url), callback=self.get_list_of_flat_links)

    def get_list_of_flat_links(self,response):
        flat_links = response.xpath('//div[@data-name="LinkArea"]/a')
        prices = response.xpath(f'//div[@data-name="LinkArea"]//span[@data-mark="MainPrice"]/span/text()').extract()
        i = 0
        for link in flat_links:
            link = link.attrib['href']
            price = prices[i]
            i+=1
            yield scrapy.Request(url=get_url(link), callback=self.parse_flat,cb_kwargs={'price':price,'url':link})

    def parse_flat(self,response,price,url):
        item = SpiderCianItem()
        item['address'] = ' '.join(response.xpath('//address//a/text()').extract())
        item['price'] = price[:-2].replace(' ','')
        item['url'] = url
        ret = response.xpath('//script[contains(text(),"coordinates")]/text()').extract()[0]
        coordinates = eval(re.findall('(?<=coordinates\":)[^}]*}',ret)[0])
        item['coordinates'] = coordinates
        yield item
