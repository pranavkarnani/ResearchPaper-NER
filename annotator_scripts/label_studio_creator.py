from fuzzywuzzy import fuzz
import pandas as pd
from pojo_label_studio import *
import json
import time
import glob
import nltk
# nltk.download('stopwords')

from nltk.corpus import stopwords

sheet_path = 'Keyword Lists.xlsx'
tokenized_papers_path = ''

class LabelStudioCreator:
    def __init__(self, filename):
        self.filename = filename.split('/')[-1]
        self.word_to_named_entity = {}
        json_file = json.load(open(tokenized_papers_path + filename + '.json', 'r', encoding='utf-8'))
        self.lines = json_file['text']
        self.lines = self.lines.replace('\n ', '')

    def _read_sheets(self):
        datasets = pd.read_excel(sheet_path, sheet_name='Datasets', converters={'Datasets':str})
        metrics = pd.read_excel(sheet_path, sheet_name='Metrics', converters={'Metrics':str})
        models = pd.read_excel(sheet_path, sheet_name='Models', converters={'Models':str})
        methods = pd.read_excel(sheet_path, sheet_name='Methods', converters={'Methods':str})
        hyperparameters = pd.read_excel(sheet_path, sheet_name='Hyperparameters', converters={'Hyperparameters':str})
        return datasets, metrics, models, methods, hyperparameters

    def _assign_entity(self, word, arr, entity, startIndex, endIndex):
        if word in self.word_to_named_entity:
            value = Value(startIndex, endIndex, word, [entity])
            return value
        for ele in arr:
            if fuzz.ratio(str(ele), word) > 85:
                self.word_to_named_entity[word] = entity
                value = Value(startIndex, endIndex, word, [entity])
                return value
        return None

    # def _assign_entity_using_rapidfuzz(self, word, arr, entity, startIndex, endIndex):
    #     if word in self.word_to_named_entity and self.word_to_named_entity[word] != 'O':
    #         value = Value(startIndex, endIndex, word, [entity])
    #         return value

    #     model = PolyFuzz(self.rapidfuzz_matcher).match(arr, [word])
    #     if True in (ele >= 0.85 for ele in model.get_matches()['Similarity'].tolist()):
    #         self.word_to_named_entity[word] = entity
    #         value = Value(startIndex, endIndex, word, [entity])
    #         return value

    def __call__(self):
        datasets, metrics, models, methods, hyperparameters = self._read_sheets()
        startIndex = 0
        results = []

        wordList = self.lines.split(' ')
        for word in enumerate(wordList):
            endIndex = startIndex + len(word)
            value = None
            if word not in stopwords:
                value = self._assign_entity(word, datasets['Datasets'].tolist(), 'DatasetName', startIndex, endIndex)
                value = self._assign_entity(word, metrics['Metrics'].tolist(), 'MetricName', startIndex, endIndex) if value is None else value
                value = self._assign_entity(word, models['Models'].tolist(), 'MethodName', startIndex, endIndex) if value is None else value
                value = self._assign_entity(word, methods['Methods'].tolist(), 'TaskName', startIndex, endIndex) if value is None else value
                value = self._assign_entity(word, hyperparameters['Hyperparameters'].tolist(), 'HyperparameterName', startIndex, endIndex) if value is None else value

            startIndex = endIndex + 1    
            if value is None:
                stopwords.add(word)
                continue
            result = Result(value, hash(word))
            results.append(result)

        data = Data(self.lines, int(self.filename))
        completedBy = CompletedBy(int(self.filename) + 1)
        annotation = Annotation(int(self.filename) + 1, completedBy, results)
        labelStudio = LabelStudio(int(self.filename) + 1, data, [annotation], [])
        with open('tokenized_papers_annotated/' + self.filename + '_annotated.json', 'w', encoding='utf-8') as f:
            json_data = json.dumps(labelStudio.__dict__, default=lambda o: o.__dict__)
            f.write("[")
            f.write(json_data)
            f.write("]")

if __name__ == '__main__':
    start_time = time.time()
    files = sorted(glob.glob('tokenized_papers/*.json'), key = lambda x: int(x.strip('.json').strip('tokenized_papers/')))
    stopwords = set(stopwords.words('english'))

    with open('/Users/pranavkarnani/ANLP/stopwords.txt', 'r') as f:
        extra = f.readlines()

    extra = set(extra)
    stopwords = stopwords.union(extra)

    for file in files[0:20]:
        print(file)
        lsjc = LabelStudioCreator(file.split('.')[0])
        lsjc()
        end_time = time.time()
        print((end_time - start_time))
