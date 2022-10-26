import os
import json
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English

papers_text_path = 'paper_text/'
tokenized_papers_path = 'tokenized_papers/'

class TokenizeAndCreateJson():
    def __init__(self):
        nlp = English()
        self.tokenizer = Tokenizer(nlp.vocab)
        self.paper = {}
        self.paper["text"] = ""

    def __call__(self, num_of_papers):
        for i, file in enumerate(sorted(os.listdir(papers_text_path), key = lambda x: int(x.strip('.txt')))[5042:]):
            self.paper["text"] = ""
            print('Processing paper', i)
            if i >= num_of_papers:
                break
            print(file)
            temp = self.tokenizer(open(papers_text_path + file, encoding="utf-8").read())
            with open(tokenized_papers_path + file.strip('.txt') + ".json", "w", encoding="utf-8") as f:
                for token in temp:
                    self.paper["text"] += token.text + " "
                self.paper["paperid"] = file.strip('.txt')
                json_object = json.dumps(self.paper)
                f.write(json_object)

if __name__ == '__main__':
    tacj = TokenizeAndCreateJson()
    tacj(10000)