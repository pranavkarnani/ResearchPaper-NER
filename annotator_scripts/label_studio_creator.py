from fuzzywuzzy import fuzz
import pandas as pd
from pojo_label_studio import *
import json
import glob
import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords

tokenized_papers_path = 'data/tokenized/'

class LabelStudioCreator:
    def __init__(self, filename, stopwords):
        self.filename = filename.split('/')[-1]
        self.word_to_named_entity = {}
        json_file = json.load(open(tokenized_papers_path + filename + '.json', 'r', encoding='utf-8'))
        self.lines = json_file['text']
        self.lines = self.lines.replace('\n ', '')
        self.stopwords = stopwords

    def _read_sheets(self):
        sheet_path = 'data/dataset/'
        datasets = pd.read_csv(sheet_path + 'Task_Names.csv')['Task_Names']        
        metrics = pd.read_csv(sheet_path + 'Datasets.csv')['Datasets'].unique()
        models = pd.read_csv(sheet_path + 'Models.csv')['Models'].unique()
        methods = pd.read_csv(sheet_path + 'Metrics.csv')['Metrics'].unique()
        hyperparameters = pd.read_csv(sheet_path + 'pytorch_hyperparams.csv')['hyperparameter'].unique()
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

    def __call__(self):
        datasets, metrics, models, methods, hyperparameters = self._read_sheets()
        startIndex = 0
        results = []

        wordList = self.lines.split(' ')
        for word in enumerate(wordList):
            endIndex = startIndex + len(word)
            value = None
            if word not in self.stopwords:
                value = self._assign_entity(word, datasets.tolist(), 'DatasetName', startIndex, endIndex)
                value = self._assign_entity(word, metrics.tolist(), 'MetricName', startIndex, endIndex) if value is None else value
                value = self._assign_entity(word, models.tolist(), 'MethodName', startIndex, endIndex) if value is None else value
                value = self._assign_entity(word, methods.tolist(), 'TaskName', startIndex, endIndex) if value is None else value
                value = self._assign_entity(word, hyperparameters.tolist(), 'HyperparameterName', startIndex, endIndex) if value is None else value

            startIndex = endIndex + 1    
            if value is None:
                self.stopwords.add(word)
                continue
            result = Result(value, hash(word))
            results.append(result)

        data = Data(self.lines, int(self.filename))
        completedBy = CompletedBy(int(self.filename) + 1)
        annotation = Annotation(int(self.filename) + 1, completedBy, results)
        labelStudio = LabelStudio(int(self.filename) + 1, data, [annotation], [])
        with open(tokenized_papers_path + self.filename + '_annotated.json', 'w', encoding='utf-8') as f:
            json_data = json.dumps(labelStudio.__dict__, default=lambda o: o.__dict__)
            f.write("[")
            f.write(json_data)
            f.write("]")


def create_labelStudio_json(num_files):
    files = sorted(glob.glob(tokenized_papers_path + '*.json'), key = lambda x: int(x.strip('.json').strip(tokenized_papers_path)))
    stopwords = set(stopwords.words('english'))

    with open('stopwords.txt', 'r') as f:
        extra = f.readlines()

    extra = set(extra)
    stopwords = stopwords.union(extra)

    for file in files[0:num_files]:
        print(file)
        lsjc = LabelStudioCreator(file.split('.')[0], stopwords)
        lsjc()