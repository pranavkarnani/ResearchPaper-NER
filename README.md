# ResearchPaper-NER
by Pranav Karnani, Bandish Parikh, Faizan Khan

### File Structure
1. Crawlers - A web crawler which extracts all research papers on ACL Anthology on and after 2010.
            - A separate web crawler, which extracts information from the PyTorch and Huggingface about Hyperparameters
            - Another scripts which scraped commonly used datasets, metrics, tasks from papers with code.
            
2. Annotator Scripts - An automated annotator, which automatically annotated the research papers for us.
3. Training model - A set of notebooks highlighting our modeling process

PS: The annotator scripts can be made robust by cleaning the keywords extracted from the crawlers


### Sequence to run the scripts:
1. Run all the crawlers by running the main.py file
2. Run the annotator script pipeline
3. Use the notebooks in the training model directory to train models

You will find more information in the README's of each respective folder
