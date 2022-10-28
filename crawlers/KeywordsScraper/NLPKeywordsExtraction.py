import os
import json
import pandas as pd

def get_papers_from_code_data():

    data = json.load(open("./data/dataset/evaluation-tables.json",'rb'))

    all_task_names = []
    all_datasets = []
    all_model_names = []
    all_metrics = []

    try:
        if not os.path.exists("./data/"):
            os.makedirs("./data/")

        if not os.path.exists("./data/dataset"):
            os.makedirs("./data/dataset/")
    except:
        pass

    path = "./data/dataset/"

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

    df_tasks.to_csv(path + "Task_Names.csv")
    df_data.to_csv(path + "Datasets.csv")
    df_models.to_csv(path + "Models.csv")
    df_metrics.to_csv(path + "Metrics.csv")




