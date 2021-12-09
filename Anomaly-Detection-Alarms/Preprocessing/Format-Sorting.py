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
config = load_config("data_loader_format.yaml")
# load data
aggregated_alarms_interval = pd.read_csv(os.path.join(config["data_directory"], config["data_name"]))

aggregated_alarms_interval = aggregated_alarms_interval.iloc[:, 1:]

type_list = sorted(aggregated_alarms_interval[config["type"]].unique())

aggregated_alarms_interval[config["occurrence_time"]] = pd.to_datetime(aggregated_alarms_interval[config["occurrence_time"]])
aggregated_alarms_interval_sort = pd.DataFrame(columns=aggregated_alarms_interval.columns)

for type in type_list:
    aggregated_alarms_interval_type = aggregated_alarms_interval[aggregated_alarms_interval[config["type"]] == type]
    cell_list = sorted(list(aggregated_alarms_interval_type[config['cell_id']].unique()))
    for cell in cell_list:
        aggregated_alarms_interval_type_cell = aggregated_alarms_interval_type[aggregated_alarms_interval_type[config['cell_id']] == cell]
        interval_list = sorted(aggregated_alarms_interval_type_cell[config["interval_number"]].unique())
        for i in range(len(interval_list)):
            aggregated_alarms_interval_type_cell_int = aggregated_alarms_interval_type_cell[aggregated_alarms_interval_type_cell[config['interval_number']] == interval_list[i]]
            aggregated_alarms_interval_type_cell_int = aggregated_alarms_interval_type_cell_int.reset_index(drop=True)
            for j in range(len(aggregated_alarms_interval_type_cell_int)):
                if j != 0:
                    aggregated_alarms_interval_type_cell_int.loc[j, config['inter_arrival_time']] = aggregated_alarms_interval_type_cell_int.loc[j, config['occurrence_time']] - aggregated_alarms_interval_type_cell_int.loc[j-1, config['occurrence_time']]
                    aggregated_alarms_interval_type_cell_int.loc[j, config['inter_arrival_time_min']] = round(aggregated_alarms_interval_type_cell_int.loc[j, config['inter_arrival_time']].seconds / 60, 2)
            aggregated_alarms_interval_sort = pd.concat([aggregated_alarms_interval_sort, aggregated_alarms_interval_type_cell_int], axis=0)


aggregated_alarms_interval_sort.to_csv(os.path.join(config["data_directory"], config["data_saved"]))
