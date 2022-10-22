import os
import csv
import time
import scrapy
import logging
import unicodedata
import requests

from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.spidermiddlewares.httperror import HttpError

from twisted.internet import reactor
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError
from twisted.internet.defer import inlineCallbacks

from collections import defaultdict
from utils.strings import *
from bs4 import BeautifulSoup


class PaperSpider(scrapy.Spider):
    name = "paper-scraper"
    domain = DOMAIN_URL
    developerMaster = set()
    organizationMaster = set()
    err_pages = []

    def start_requests(self):
        
        self.setup()
        
        # For hugging face
        start_urls = []
        
        start_urls.append("https://huggingface.co/docs/transformers/model_doc/gpt2")

        # start_urls = []
        # start_urls.append("https://pytorch.org/docs/stable/nn.html")
        logging.log(logging.INFO, "Loading requests")
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_nn_modules, errback=self.errback_httpbin, dont_filter=True)


    # //dd[@class='field-odd']/ul[@class='simple']/li/p/strong
    def parse_nn_modules(self, response):

        # For hugging face
        fpath = "//a[@class='text-gray-500 pr-2 hover:text-black dark:hover:text-gray-300 py-1 transform transition-all hover:translate-x-px first:mt-1 last:mb-4 pl-2 ml-6']/@href"
        
        # For pytorch
        print('Response', response)

        # fpath = "//table[@class='longtable docutils colwidths-auto align-default']/tbody/tr[@class='row-odd']/td/p/a[@class='reference internal has-code']/@href"
        url_links = response.xpath(fpath).getall()
        print('############', url_links)
        for i in url_links:
            url = DOMAIN_URL + i
            print('#####', url)
            yield scrapy.Request(url = url, callback=self.parse_module, errback=self.errback_httpbin, dont_filter=True)

    def parse_module(self, response):

        # For hugging face
        module_name = response.xpath("//h1[@class='relative group']/span/text()").get()
        module_params = response.xpath("//span[@class='group flex space-x-1.5 items-start']/span/strong/text()").getall()

        # For pytorch
        # module_name = response.xpath("//h1/text()").get()
        # module_params = response.xpath("//dd[@class='field-odd']/ul[@class='simple']/li/p/strong/text()").getall()
        print(module_name)
        print(module_params)

        if module_params != None and module_name != None:
            with open('hyperparams/hyperparams.csv', 'a') as f:
                for i in module_params:
                    writer = csv.writer(f)
                    row = [module_name, i]
                    writer.writerow(row)
        
   
    def errback_httpbin(self, failure):
        url = ""
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            url = response.url

        elif failure.check(DNSLookupError):
            request = failure.request
            url = request.url

        elif failure.check(TimeoutError):
            request = failure.request
            url = request.url

        self.err_pages.append(url)

    def closed(self, message):
        print('Spider closed!')

    def setup(self):
        print('Setup complete!')

        
def getRunner():
    runner = CrawlerRunner({
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'RETRY_TIMES': 0,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
        },
        'USER_AGENTS': [
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/57.0.2987.110 '
             'Safari/537.36'),
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/61.0.3163.79 '
             'Safari/537.36'),
            ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
             'Gecko/20100101 '
             'Firefox/55.0'),
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/61.0.3163.91 '
             'Safari/537.36'),
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/62.0.3202.89 '
             'Safari/537.36'),
            ('Mozilla/5.0 (X11; Linux x86_64) '
             'AppleWebKit/537.36 (KHTML, like Gecko) '
             'Chrome/63.0.3239.108 '
             'Safari/537.36')]
    })
    return runner

@inlineCallbacks
def crawl_url():
    print('crawling')
    configure_logging()
    s1 = getRunner()
    yield s1.crawl(PaperSpider)
    reactor.stop()
