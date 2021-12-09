import pandas as pd
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
config = load_config("data_loader_aggregated_sort.yaml")
# load data
aggregated_alarms_sort = pd.read_csv(os.path.join(config["data_directory"], config["data_name"]))
aggregated_alarms_sort=aggregated_alarms_sort.iloc[:,1:]
intervals = pd.read_csv(os.path.join(config["data_directory"], config["interval_saved"]))
intervals=intervals.iloc[:,1:]
intervals[config["interval_lower_limit"]] = pd.to_datetime(intervals[config["interval_lower_limit"]])
intervals[config["interval_upper_limit"]] = pd.to_datetime(intervals[config["interval_upper_limit"]])

aggregated_alarms_interval= pd.DataFrame(columns=['TYPE', 'CELL_ID', 'ID', 'INTERVAL_NUMBER', 'INTERVAL_LOWER_LIMIT', 'INTERVAL_UPPER_LIMIT','NUMBER_OF_ALARMS', 'ALARM_NUMBER', 'CREATED_TIME', 'OCCURRENCE_TIME', 'DESCRIPTION','SEVERITY'])
#create a function for sort or not necessary?
type_list=sorted(aggregated_alarms_sort[config["type"]].unique())
aggregated_alarms_sort[config["occurrence_time"]] = pd.to_datetime(aggregated_alarms_sort[config["occurrence_time"]])

#How to import LLimit and ULimit?
for type in type_list:
    aggregated_alarms_sort_type= aggregated_alarms_sort[aggregated_alarms_sort[config["type"]] == type]
    cell_list = sorted(aggregated_alarms_sort[config["cell_id"]].unique())
    for cell in cell_list:
        aggregated_alarms_sort_type_cell = aggregated_alarms_sort_type[aggregated_alarms_sort_type[config["cell_id"]] == cell]
        aggregated_alarms_sort_type_cell = aggregated_alarms_sort_type_cell.reset_index(drop=True)
        if len(aggregated_alarms_sort_type_cell) != 0:
            for i in range(len(aggregated_alarms_sort_type_cell)):
                for l in range(len(intervals[config['interval_lower_limit']])):
                    if (aggregated_alarms_sort_type_cell.loc[i, config["occurrence_time"]] < intervals[config['interval_upper_limit']][l]) & (aggregated_alarms_sort_type_cell.loc[i, config["occurrence_time"]] >= intervals[config['interval_lower_limit']][l]):
                        aggregated_alarms_interval = aggregated_alarms_interval.append({'TYPE': type, 'CELL_ID': cell, 'ID': aggregated_alarms_sort_type_cell.loc[i, config["id"]], 'INTERVAL_NUMBER': l + 1,
                             'INTERVAL_LOWER_LIMIT':  intervals[config['interval_lower_limit']][l], 'INTERVAL_UPPER_LIMIT':  intervals[config['interval_upper_limit']][l],
                             'NUMBER_OF_ALARMS': len(aggregated_alarms_sort_type_cell), 'ALARM_NUMBER': i + 1,
                             'CREATED_TIME': aggregated_alarms_sort_type_cell.loc[i, config["created_time"]],
                             'OCCURRENCE_TIME': aggregated_alarms_sort_type_cell.loc[i, config["occurrence_time"]],
                             'DESCRIPTION': aggregated_alarms_sort_type_cell.loc[i, config["description"]], 'SEVERITY': aggregated_alarms_sort_type_cell.loc[i, config["severity"]]},ignore_index=True)


#aggregated_alarms_interval.to_csv('C:\\Users\\User\\Desktop\\B-Yond\\New_paper-Alarms\\Approach3-Sample2\\aggregated_alarms_interval.csv')

aggregated_alarms_interval.to_csv(os.path.join(config["data_directory"], config["data_saved"]))
