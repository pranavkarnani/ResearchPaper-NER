from bs4 import BeautifulSoup as bs
import os
import requests
import csv

def scrape_pytorch():
    
    try:
        if not os.path.exists("data/"):
            os.makedirs("data/")

        if not os.path.exists("./data/dataset"):
            os.makedirs("./data/dataset/")
    except:
        pass

    file_pytorch = open('./data/dataset/pytorch_hyperparams.csv', 'w')
    writer = csv.writer(file_pytorch)
    writer.writerow(['module', 'hyperparameter'])

    base_url = "https://pytorch.org/docs/stable/nn.html"
    response = requests.get(base_url)
    soup = bs(response.text, 'html.parser')
    
    nn_urls = []
    for a in soup.find_all("a", href=True):
        nn_urls.append("https://pytorch.org/docs/stable/" + a["href"]) if str(a["href"]).startswith("generated/torch.nn") else None
    
    for url in nn_urls:
        temp_response = requests.get(url)
        ssoup = bs(temp_response.text, 'html.parser')

        module = ssoup.find('h1').text[:-1]
        for ele in ssoup.find_all("dl", {"class": "field-list simple"}):
            for hyperparam in ele.find_all("strong"):
                data = [module, hyperparam.text]
                writer.writerow(data)


    file_pytorch.close()