import os

from utils.strings import *
from scraper.master import crawl_url
from twisted.internet import reactor

def setup():
    try:
        if not os.path.exists("data/"):
            os.makedirs("data/")

        if not os.path.exists("./data/dataset"):
            os.makedirs("./data/dataset")
    except:
        pass


def crawl_huggingface():
    setup()
    crawl_url()
    reactor.run()