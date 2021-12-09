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
config = load_config("data_loader_originaldata.yaml")
# load data
alarms_original = pd.read_csv(os.path.join(config["data_directory"], config["data_name"]))

'correct way to load data?'
'Replace?'
'''Clean Column TYPE in the data: Merge other and Other//Communications alarm and communicationsAlarm//qualityOfServiceAlarm 
and Quality Of Service//processingErrorAlarm and PROCESSING ERROR
'''
for key, value in config['replace'].items():
    alarms_original[config['type']]=[str(x).replace(key, value) for x in alarms_original['TYPE']]


'''Sample extraction'''
Interval=[pd.Timestamp(config["interval_start"]),pd.Timestamp(config["interval_end"])]
alarms_original[config["occurrence_time"]]=pd.to_datetime(alarms_original[config["occurrence_time"]])

alarms_sample=alarms_original[(alarms_original[config["occurrence_time"]]<=Interval[1]) & (alarms_original[config["occurrence_time"]]>Interval[0])]

'Save it or add all csv files?'
alarms_sample.to_csv(os.path.join(config["data_directory"], config["data_saved"]))

