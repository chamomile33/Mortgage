#from spider_cian import *
#from spider_cian.spiders import SpiderCianItem
#from spider_cian.spiders import CityParseSpider
from twisted.internet import asyncioreactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import sys
#from spider_cian import settings as my_settings

# form = ['rooms','region','object_type','minprice','maxprice','minarea','maxarea','min_living_area','max_living_area',
#         'min_kitchen_area','max_kitchen_area','minfloor','maxfloor','floor_type','min_house_year','max_house_year']
# form_dict = {item:None for item in form}  
# form_dict['rooms'] = ['5']
# form_dict['region'] = 'Алтайский край'
# form_dict['maxfloor'] = 7

# process = CrawlerProcess(settings=get_project_settings())
# process.crawl('CityParseSpider')
# process.start()

process = CrawlerProcess(get_project_settings())
process.crawl('SpiderCianItem', url = sys.argv[1])
process.start()