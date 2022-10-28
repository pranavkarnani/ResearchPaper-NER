import os
from tokenize_and_create_json import TokenizeAndCreateJson
from label_studio_creator import create_LabelStudio_json

os.mkdir('tokenized_papers/')
tacj = TokenizeAndCreateJson()
tacj(10000)

os.mkdir('tokenized_papers_annotated')
create_LabelStudio_json()