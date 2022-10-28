from ACLScraper.main import crawl_acl
from HuggingFaceScraper.main import crawl_huggingface
from PyTorchScraper.master import scrape_pytorch
from KeywordsScraper.NLPKeywordsExtraction import get_papers_from_code_data

crawl_acl()
crawl_huggingface()
scrape_pytorch()
get_papers_from_code_data()