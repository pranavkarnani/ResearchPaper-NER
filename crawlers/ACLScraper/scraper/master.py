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
from ACLScraper.utils.strings import *
from bs4 import BeautifulSoup


class PaperSpider(scrapy.Spider):
    name = "paper-scraper"
    domain = DOMAIN_URL
    developerMaster = set()
    organizationMaster = set()
    err_pages = []

    def start_requests(self):
        
        self.setup()
        
        start_urls = []
        start_urls.append("https://aclanthology.org/")

        logging.log(logging.INFO, "Loading requests")
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_journals, errback=self.errback_httpbin, dont_filter=True)

    def parse_journals(self, response):
        urls = []
        fpath = "//table[1]/tbody/tr/td["
        for i in range(1, 14):
            url_xpath = fpath + str(i) + "]/a/@href"
            url_links = response.xpath(url_xpath).getall()
            urls.extend(url_links)

        for i in urls:
            url = DOMAIN_URL + i
            yield scrapy.Request(url = url, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)

    def parse(self, response):
        papers = response.xpath("//strong/a[@class='align-middle']/@href").getall()
        for paper in papers:
            paperUrl = DOMAIN_URL + paper
            yield scrapy.Request(url=paperUrl, callback=self.parse_paper_details, errback = self.errback_httpbin, dont_filter = True)


    def parse_paper_details(self, response, **kwargs):
        try:
            paperName = response.xpath("//h2[@id='title']/a/text()").extract()[0]
            downloadUrl = response.xpath("//a[@class='btn btn-primary']/@href").get()

            if DOMAIN_URL not in downloadUrl:
                downloadUrl = DOMAIN_URL + downloadUrl

            response = requests.get(downloadUrl)
            open("./"+paperName+".pdf", "wb").write(response.content)


        except AttributeError:
            self.err_pages.append(response.url)
        except:
            self.err_pages.append(response.url)

   
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
