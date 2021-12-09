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
config = load_config("data_loader_sample.yaml")
# load data
alarms_sample = pd.read_csv(os.path.join(config["data_directory"], config["data_name"]))
alarms_sample = alarms_sample.iloc[:, 1:]

cell_list=alarms_sample[config["cell_id"]].unique()

aggregated_alarms = pd.DataFrame(columns=alarms_sample.columns)

for cell in cell_list:
    alarms_sample_cell = alarms_sample[alarms_sample[config["cell_id"]] == cell]
    alarm_sid_list = alarms_sample_cell[config["alarm_sid"]].unique()
    for alarm_sid in alarm_sid_list:
        alarms_sample_cell_sid = alarms_sample_cell[alarms_sample_cell[config["alarm_sid"]] == alarm_sid]
        severity_list= alarms_sample_cell_sid[config["severity"]].unique()
        for severity in severity_list:
            alarms_sample_cell_sid_sev = alarms_sample_cell_sid[alarms_sample_cell_sid[config["severity"]] == severity]
            occurrence_time_list=alarms_sample_cell_sid_sev[config["occurrence_time"]].unique()
            for occurrence_time in occurrence_time_list:
                alarms_sample_cell_sid_sev_occ = alarms_sample_cell_sid_sev[alarms_sample_cell_sid_sev[config["occurrence_time"]] == occurrence_time].iloc[[0], :]
                aggregated_alarms = pd.concat([aggregated_alarms, alarms_sample_cell_sid_sev_occ], axis=0)


aggregated_alarms = aggregated_alarms.reset_index(drop=True)

aggregated_alarms.to_csv(os.path.join(config["data_directory"], config["data_saved"]))


