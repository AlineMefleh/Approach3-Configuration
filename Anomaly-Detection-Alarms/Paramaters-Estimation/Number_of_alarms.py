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
# load data
interval_alarms = pd.read_csv(os.path.join(config["data_directory"], config["data_name"]))


interval_alarms = interval_alarms.iloc[:, 1:]


'''
Build the dataframe for the number of alarms
'''
number_of_alarms = pd.DataFrame(columns=['TYPE', 'CELL_ID', 'INTERVAL_NUMBER', 'START_TIME', 'END_TIME', 'NUMBER_OF_ALARMS','WEIGHTED_NUMBER_OF_ALARMS'])

type_list = sorted(interval_alarms[config["type"]].unique())
interval_alarms[config["occurrence_time"]] = pd.to_datetime(interval_alarms[config["occurrence_time"]])
interval_alarms[config['interval_lower_limit']] = pd.to_datetime(interval_alarms[config['interval_lower_limit']])
interval_alarms[config['interval_upper_limit']] = pd.to_datetime(interval_alarms[config['interval_upper_limit']])
interval_alarms[config['created_time']] = pd.to_datetime(interval_alarms[config['created_time']])

for type in type_list:
    interval_alarms_type = interval_alarms[interval_alarms[config['type']] == type]
    cell_list = sorted(interval_alarms_type[config['cell_id']].unique())
    for cell in cell_list:
        interval_alarms_type_cell = interval_alarms_type[interval_alarms_type[config['cell_id']] == cell]
        interval_list = interval_alarms_type_cell[config['interval_number']].unique().tolist()
        for interval in interval_list:
            interval_alarms_type_cell_interval = interval_alarms_type_cell[interval_alarms_type_cell[config['interval_number']] == interval]
            interval_alarms_type_cell_interval = interval_alarms_type_cell_interval.reset_index(drop=True)
            weighted_number = 0
            for l in range(len(interval_alarms_type_cell_interval)):
                severity = interval_alarms_type_cell_interval[config['severity']][l]
                weighted_number = weighted_number + config['weights'][severity]
            number_of_alarms = number_of_alarms.append(
                {'TYPE': type, 'CELL_ID': cell, 'INTERVAL_NUMBER': interval, 'INTERVAL_LOWER_LIMIT': interval_alarms_type_cell_interval[config['interval_lower_limit']][0],
                 'INTERVAL_UPPER_LIMIT': interval_alarms_type_cell_interval[config['interval_upper_limit']][0], 'NUMBER_OF_ALARMS': len(interval_alarms_type_cell_interval),
                 'WEIGHTED_NUMBER_OF_ALARMS': weighted_number}, ignore_index=True)


config_results = load_config("data_loader_results.yaml")

writer = pd.ExcelWriter(os.path.join(config_results["data_directory"], config_results["data_name"]))
workbook = writer.book
number_of_alarms.to_excel(writer, sheet_name=config_results['sheet_number_of_alarms'])
writer.save()

