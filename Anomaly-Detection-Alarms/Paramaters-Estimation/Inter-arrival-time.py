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
inter_arrival_time = pd.DataFrame(columns=['TYPE', 'AVERAGE_INTER_ARRIVAL_TIME(min)'])
interval_alarms = pd.read_csv(os.path.join(config["data_directory"], config["data_name"]))

type_list = sorted(interval_alarms[config['type']].unique())
interval_alarms[config['occurrence_time']] = pd.to_datetime(interval_alarms[config['occurrence_time']])
interval_alarms[config['interval_lower_limit']] = pd.to_datetime(interval_alarms[config['interval_lower_limit']])
interval_alarms[config['interval_upper_limit']] = pd.to_datetime(interval_alarms[config['interval_upper_limit']])
interval_alarms[config['created_time']] = pd.to_datetime(interval_alarms[config['created_time']])

for type in type_list:
    interval_alarms_type = interval_alarms[interval_alarms[config['type']] == type]
    inter_arrival_time = inter_arrival_time.append({'TYPE': type, 'AVERAGE_INTER_ARRIVAL_TIME(min)': interval_alarms_type['INTER_ARRIVAL_TIME(min)'].mean()},ignore_index=True)

#inter_arrival_time.to_excel(writer, sheet_name='Inter-arrival time')
#writer.save()
config_results = load_config("data_loader_results.yaml")

from openpyxl import load_workbook

path_result = os.path.join(config_results["data_directory"], config_results["data_name"])
book = load_workbook(path_result)
writer_result = pd.ExcelWriter(path_result, engine='openpyxl')
writer_result.book = book

inter_arrival_time.to_excel(writer_result, sheet_name=config_results["sheet_inter_arrival_time"])
writer_result.save()
