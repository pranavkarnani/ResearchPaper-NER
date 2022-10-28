import enum
from ACLScraper.main import crawl_acl
from HuggingFaceScraper.main import crawl_huggingface
from PyTorchScraper.master import scrape_pytorch
from KeywordsScraper.NLPKeywordsExtraction import get_papers_from_code_data
from PyPDF2 import PdfReader
import glob

def convert_pdf_to_text():
    files = glob.glob('./data/pdf/*')

    for i, pdf in enumerate(files):
        reader = PdfReader(pdf)
        with open('./data/text/' + str(i) + '.txt', 'w') as f:
            for page in reader.pages:
                f.write(page.extract_pages())

crawl_acl()
crawl_huggingface()
scrape_pytorch()
get_papers_from_code_data()
convert_pdf_to_text()