from twisted.internet import asyncioreactor
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import sys

process = CrawlerProcess(get_project_settings())
process.crawl('SpiderCianItem', url = sys.argv[1])
process.start()