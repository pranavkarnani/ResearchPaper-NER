# ResearchPaper-NER
by Pranav Karnani, Bandish Parikh, Faizan Khan

## File Structure
1. Crawlers - A web crawler which extracts all research papers on ACL Anthology on and after 2010.
            - A separate web crawler, which extracts information from the PyTorch and Huggingface about Hyperparameters
            - Another scripts which scraped commonly used datasets, metrics, tasks from papers with code.
            
2. Annotator Scripts - An automated annotator, which automatically annotated the research papers for us.
3. Training model - A set of notebooks highlighting our modeling process

PS: The annotator scripts can be made robust by cleaning the keywords extracted from the crawlers


## Sequence to run the scripts:
1. Run all the crawlers by running the main.py file
2. Run the annotator script pipeline
3. Use the notebooks in the training model directory to train models

## Crawlers

### Steps to Run:
1. Download the dataset from papers with code in the link - https://production-media.paperswithcode.com/about/evaluation-tables.json.gz
2. Move the downloaded file inside the ResearchPaper-NER directory and rename it to evaluation-tables.json
3. Run the following commands: <br />
   3.1 python crawlers/ACLScraper/main.py <br />
   3.2 python crawlers/HuggingFaceScraper/main.py <br />
   3.3 python crawlers/main.py <br />
         
### Outputs:
1. All papers from ACLAnthonlogy.org would be downloaded in the folder named data. The pdf and text files will be stored in different directories.
2. The hyperparameters, keywords, datasets, metrics and tasks would be downloaded as separate CSV files in the dataset directory inside data


## Annotator Scripts

### Steps to Run
1. Run the command - python annotator_scripts/main.py

### Output
1. All downloaded papers will be tokenized using spacy, annotated automatically for consumption by Label Studio
2. These papers will be stored in directory named - tokenized inside the data directory

