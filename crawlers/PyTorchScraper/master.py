from bs4 import BeautifulSoup as bs
import requests
import csv


def scrape_pytorch():
    
    file_pytorch = open('./pytorch_hyperparams.csv', 'w')
    writer = csv.writer(file_pytorch)
    writer.writerow(['module', 'hyperparameter'])
    # start_urls.append("https://huggingface.co/docs/transformers/model_doc/gpt2")
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