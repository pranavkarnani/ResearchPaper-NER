from PyTorchScraper.master import scrape_pytorch
from KeywordsScraper.NLPKeywordsExtraction import get_papers_from_code_data
from PyPDF2 import PdfReader
import glob
import os

def convert_pdf_to_text():
    files = glob.glob('./data/pdf/*')

    for i, pdf in enumerate(files):
        try:
            reader = PdfReader(pdf)
            with open('./data/text/' + str(i) + '.txt', 'w') as f:
                for page in reader.pages:
                    try:
                        f.write(page.extract_text())
                    except:
                        print('./data/text/' + str(i) + '.txt')
                        os.remove('./data/text/' + str(i) + '.txt')
        except:
            continue

scrape_pytorch()
get_papers_from_code_data()
convert_pdf_to_text()