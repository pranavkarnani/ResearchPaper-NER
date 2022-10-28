import os
import csv

from HuggingFaceScraper.utils.strings import *
from HuggingFaceScraper.scraper.master import crawl_url
from twisted.internet import reactor

def setup():
    try:
        if not os.path.exists("./hyperparams"):
            os.makedirs("./hyperparams")

    except:
        pass

    file = open("./hyperparams/hyperparams.csv", "w")
    file.close()

    file = open("./hyperparams/errors.csv", "w")
    file.close()

    with open("./hyperparams/hyperparams.csv", 'a', encoding='utf8', newline='') as papers:
        tsv_writer = csv.writer(papers, delimiter=',', lineterminator='\n')
        tsv_writer.writerow(['module', 'parameter'])

def crawl_huggingface():
    setup()
    crawl_url()
    reactor.run()