import pandas as pd
import numpy as np
import yaml
import os

# folder to load config file
CONFIG_PATH = "./Data initializers/"
# Function to load yaml configuration file
def load_config(config_name):
    with open(os.path.join(CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)
    return config
config = load_config("data_loader_aggregated.yaml")
# load data
aggregated_alarms = pd.read_csv(os.path.join(config["data_directory"], config["data_name"]))
aggregated_alarms=aggregated_alarms.iloc[:,1:]
cell_list= sorted(list(aggregated_alarms[config['cell_id']].unique()))
aggregated_alarms_sort= pd.DataFrame(columns=aggregated_alarms.columns)

for cell in cell_list:
    aggregated_alarms_cell = aggregated_alarms[aggregated_alarms[config['cell_id']] == cell]
    aggregated_alarms_cell_sort = aggregated_alarms_cell.sort_values(config["occurrence_time"])
    aggregated_alarms_sort = pd.concat([aggregated_alarms_sort, aggregated_alarms_cell_sort], axis=0)

aggregated_alarms_sort.to_csv(os.path.join(config["data_directory"], config["data_saved"]))
git