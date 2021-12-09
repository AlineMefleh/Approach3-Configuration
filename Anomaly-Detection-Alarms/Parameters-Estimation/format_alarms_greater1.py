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

config = load_config("data_loader_format_sort.yaml")

interval_alarms = pd.read_csv(os.path.join(config["data_directory"], config["data_name"]))
interval_alarms = interval_alarms.iloc[:, 1:]

type_list = sorted(interval_alarms[config['type']].unique())

interval_alarms[config['occurrence_time']] = pd.to_datetime(interval_alarms[config['occurrence_time']])
interval_alarms[config['interval_lower_limit']] = pd.to_datetime(interval_alarms[config['interval_lower_limit']])
interval_alarms[config['interval_upper_limit']] = pd.to_datetime(interval_alarms[config['interval_upper_limit']])
interval_alarms[config['created_time']] = pd.to_datetime(interval_alarms[config['created_time']])

type_description = pd.DataFrame(columns=['TYPE', 'CELL_ID', 'INTERVAL_NUMBER', 'INTERVAL_LOWER_LIMIT', 'INTERVAL_UPPER_LIMIT', 'DESCRIPTION'])

for type in type_list:
    interval_alarms_type = interval_alarms[interval_alarms[config['type']] == type]
    cell_list = interval_alarms_type[config['cell_id']].unique()
    for cell in cell_list:
        interval_alarms_type_cell= interval_alarms_type[interval_alarms_type[config['cell_id']] == cell]
        interval_list = interval_alarms_type_cell[config['interval_number']].unique()
        for interval in interval_list:
            interval_alarms_type_cell_interval = interval_alarms_type_cell[interval_alarms_type_cell[config['interval_number']] == interval]
            interval_alarms_type_cell_interval = interval_alarms_type_cell_interval.reset_index(drop=True)
            if len(interval_alarms_type_cell_interval) == 1:
                continue
            else:
                for j in range(len(interval_alarms_type_cell_interval)):
                    type_description = type_description.append({'TYPE': type, 'CELL_ID': cell, 'INTERVAL_NUMBER': interval,
                                    'INTERVAL_LOWER_LIMIT': interval_alarms_type_cell_interval[config['interval_lower_limit']][j],
                                    'INTERVAL_UPPER_LIMIT': interval_alarms_type_cell_interval[config['interval_upper_limit']][j],
                                    'DESCRIPTION': interval_alarms_type_cell_interval[config['description']][j]}, ignore_index=True)

'''from openpyxl import load_workbook

path_result = r"C:\\Users\\User\\Desktop\\B-Yond\\New_paper-Alarms\\Approach3-Sample2\\Results.xlsx"
book = load_workbook(path_result)
writer_result = pd.ExcelWriter(path_result, engine='openpyxl')
writer_result.book = book
type_description.to_excel(writer_result, sheet_name='Type-Description')
writer_result.save()
'''