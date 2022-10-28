import os
from tokenize_and_create_json import TokenizeAndCreateJson
from label_studio_creator import create_labelStudio_json
num_files = 10

os.mkdir('data/tokenized_papers/')
tacj = TokenizeAndCreateJson()
tacj(num_files)

os.mkdir('tokenized_papers_annotated')
create_labelStudio_json(num_files)