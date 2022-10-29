import os
from tokenize_and_create_json import TokenizeAndCreateJson
from label_studio_creator import create_labelStudio_json
num_files = 10
if not os.path.exists("./data/tokenized/"):
    os.makedirs("./data/tokenized/")
tacj = TokenizeAndCreateJson()
tacj(num_files)

create_labelStudio_json(num_files)