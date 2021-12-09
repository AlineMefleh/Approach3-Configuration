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

#U4= pd.DataFrame(columns=['Type','Cell_ID','ID','Interval Number','Interval Lower Limit','Interval Upper Limit','Number of alarms','Alarm Number','Created time','Occurrence time','Description','Severity'])
#create a function for sort or not necessary?
#Type=sorted(data[config["type"]].unique())
aggregated_alarms_sort[config['occurrence_time']]=pd.to_datetime(aggregated_alarms_sort[config["occurrence_time"]])
interval_length = config["interval_length"]  # Time interval of 30 minutes
interval_window = config["interval_window"]
first_occurrence = sorted(aggregated_alarms_sort[config["occurrence_time"]])[0]
last_occurrence = sorted(aggregated_alarms_sort[config["occurrence_time"]])[-1]
lower_limit = []
upper_limit = []
lower_limit.append(first_occurrence)
upper_limit.append(first_occurrence + timedelta(minutes=config["interval_length"]))

while upper_limit[-1] < last_occurrence:
    lower_limit.append(lower_limit[-1] + timedelta(minutes=config["interval_window"]))
    upper_limit.append(lower_limit[-1] + timedelta(minutes=config["interval_length"]))

#How to save the results for future use?
intervals=pd.concat([pd.Series(lower_limit), pd.Series(upper_limit)], axis=config['axis'])
intervals.columns=['lower_limit','upper_limit']

intervals.to_csv(os.path.join(config["data_directory"], config["interval_saved"]))