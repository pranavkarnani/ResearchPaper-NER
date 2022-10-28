import json
import requests
import pandas as pd

def get_papers_from_code_data():

    data = json.load(open("evaluation-tables.json",'rb'))

    all_task_names = []
    all_datasets = []
    all_model_names = []
    all_metrics = []

    for row in data:
        if 'Natural Language Processing' in row['categories']:
            if 'datasets' in row.keys():
                all_task_names.append(row['task'])
                for dataset in row['datasets']:
                    all_datasets.append(dataset['dataset'])
                    if 'sota' in dataset.keys():
                        for models in dataset['sota']['rows']:
                            all_model_names.append(models['model_name'])
                            all_metrics.extend(list(models['metrics'].keys()))
            elif 'subtasks' in row.keys():
                for subtask in row['subtasks']:
                    all_task_names.append(subtask['task'])

    df_tasks = pd.DataFrame({"Task_Names":list(set(all_task_names))})
    df_data = pd.DataFrame({"Datasets":list(set(all_datasets))})
    df_models = pd.DataFrame({"Models":list(set(all_model_names))})
    df_metrics = pd.DataFrame({"Metrics":list(set(all_metrics))})

    df_tasks.to_csv("Task_Names.csv")
    df_data.to_csv("Datasets.csv")
    df_models.to_csv("Models.csv")
    df_metrics.to_csv("Metrics.csv")




