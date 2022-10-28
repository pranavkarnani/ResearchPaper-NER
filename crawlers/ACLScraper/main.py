import os
import csv

from ACLScraper.utils.strings import *
from ACLScraper.scraper.master import crawl_url
from twisted.internet import reactor

def setup():
    try:
        if not os.path.exists("./papers"):
            os.makedirs("./papers")

    except:
        pass

    file = open("./papers/papers.tsv", "w")
    file.close()

    file = open("./papers/errors.tsv", "w")
    file.close()

    with open("./papers/papers.tsv", 'a', encoding='utf8', newline='') as papers:
        tsv_writer = csv.writer(papers, delimiter='\t', lineterminator='\n')
        tsv_writer.writerow([paperKeys['name'], paperKeys['url'], paperKeys['download'], paperKeys['abstract']])

def crawl_acl():
    setup()
    crawl_url()
    reactor.run()