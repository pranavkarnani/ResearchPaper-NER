import os
import csv

from ACLScraper.utils.strings import *
from ACLScraper.scraper.master import crawl_url
from twisted.internet import reactor

def setup():
    try:
        if not os.path.exists("./data/"):
            os.makedirs("./data/")

        if not os.path.exists("./data/text"):
            os.makedirs("./data/text")

        if not os.path.exists("./data/pdf"):
            os.makedirs("./data/pdf")
    except:
        pass


def crawl_acl():
    setup()
    crawl_url()
    reactor.run()