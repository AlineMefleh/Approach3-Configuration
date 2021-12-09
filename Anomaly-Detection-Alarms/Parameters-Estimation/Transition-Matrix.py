import pandas as pd
import numpy as np
import time,datetime
from datetime import datetime, timedelta
import yaml
import os

# folder to load config file
CONFIG_PATH = "./Data initializers/"
# Function to load yaml configuration file
def load_config(config_name):
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config

config = load_config("data_loader_results.yaml")
# load data
type_description = pd.read_excel(os.path.join(config["data_directory"], config["data_name"]),sheet_name=config['sheet_type_description'])

type_list = sorted(type_description['TYPE'].unique())

for t in range(len(type_list)):
    type= type_description[type_description[config['type']] == type_list[t]]
    description = sorted(type[config['description']].unique())
    cell_list= type[config['cell_id']].unique()
    Matrix = np.zeros(shape=(len(description), len(description)), dtype=float)
    for i in range(len(description)):
        description_number = 0
        for cell in cell_list:
            type_cell = type[type[config['cell_id']] == cell]
            interval_list = type_cell[config['cell_id']].unique()
            for interval in interval_list:
                type_cell_interval = type_cell[type_cell[config['interval_number']] == interval]
                type_cell_interval = type_cell_interval.reset_index(drop=True)
                for l in range(len(type_cell_interval) - 1):
                    if (type_cell_interval.loc[l, config['description']] == description[i]):
                        description_number = description_number + 1
        for j in range(len(description)):
            transition_number = 0
            for cell in cell_list:
                type_cell = type[type[config['cell_id']] == cell]
                interval_list = type_cell[config['interval_number']].unique()
                for interval in interval_list:
                    type_cell_interval = type_cell[type_cell[config['interval_number']] == interval]
                    type_cell_interval = type_cell_interval.reset_index(drop=True)
                    for l in range(len(type_cell_interval) - 1):
                        if (type_cell_interval.loc[l, config['description']] == description[i]) & (type_cell_interval.loc[l + 1, config['description']] == description[j]):
                            transition_number = transition_number + 1
            if description_number == 0:
                if i == j:
                    Matrix[i][j] = 1
                else:
                    Matrix[i][j] = 0
            else:
                Matrix[i][j] = transition_number / description_number
            transition_matrix = pd.DataFrame(Matrix,index=description,columns=description)

    from openpyxl import load_workbook

    path_result = r"C:\\Users\\User\\Desktop\\B-Yond\\New_paper-Alarms\\Approach3-Sample2\\Results.xlsx"
    book = load_workbook(path_result)
    writer_result = pd.ExcelWriter(path_result, engine='openpyxl')
    writer_result.book = book
    transition_matrix.to_excel(writer_result, sheet_name=str(type_list[t]))
    writer_result.save()
