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
number_of_alarms = pd.read_excel(os.path.join(config["data_directory"], config["data_name"]),sheet_name=config['sheet_number_of_alarms'])
intervals=pd.read_csv(os.path.join(config["data_directory"], config["interval_data_name"]))

type_list = sorted(number_of_alarms['TYPE'].unique())

average_number_of_alarms = pd.DataFrame(columns=['TYPE', 'AVERAGE_NUMBER_OF_ALARMS', 'AVERAGE_WEIGHTED_NUMBER_OF_ALARMS'])

for type in type_list:
    number_of_alarms_type = number_of_alarms[number_of_alarms[config['type']] == type]
    average_alarms = (number_of_alarms_type[config['number_of_alarms']].sum()) / len(intervals['lower_limit'])
    average_weighted_alarms = (number_of_alarms_type[config['weighted_number_of_alarms']].sum()) / len(intervals['lower_limit'])
    average_number_of_alarms = average_number_of_alarms.append({'TYPE': type, 'AVERAGE_NUMBER_OF_ALARMS': average_alarms, 'AVERAGE_WEIGHTED_NUMBER_OF_ALARMS': average_weighted_alarms},ignore_index=True)

#average_number_of_alarms.to_excel(writer, sheet_name='Average Number of alarms')
from openpyxl import load_workbook

path_result = os.path.join(config["data_directory"], config["data_name"])
book = load_workbook(path_result)
writer_result = pd.ExcelWriter(path_result, engine='openpyxl')
writer_result.book = book

average_number_of_alarms.to_excel(writer_result, sheet_name=config["sheet_average_number_of_alarms"])
writer_result.save()
