import pandas as pd
import numpy as np
import time,datetime
from datetime import datetime, timedelta
import yaml
import os
from scipy.stats import poisson
from scipy.stats import expon
import math
from openpyxl import load_workbook

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
average_number_of_alarms = pd.read_excel(os.path.join(config["data_directory"], config["data_name"]),sheet_name=config['sheet_average_number_of_alarms'])
inter_arrival_time = pd.read_excel(os.path.join(config["data_directory"], config["data_name"]),sheet_name=config['sheet_inter_arrival_time'])
description_index = pd.read_excel(os.path.join(config["data_directory"], config["data_name"]),sheet_name=config['sheet_index_description'])
S4 = pd.read_excel(os.path.join(config["data_directory"], config["data_name"]),sheet_name=config['sheet_S4'])

config_interval= load_config("data_loader_format_sort.yaml")
interval_alarms = pd.read_csv(os.path.join(config_interval["data_directory"], config_interval["data_name"]))
interval_alarms = interval_alarms.iloc[:, 1:]


number_of_alarms[config['poisson_probability']] = 0
number_of_alarms[config['exponential_probability']] = 0
number_of_alarms[config['transition_probability']] = 0
number_of_alarms[config['score_poisson']] = 0
number_of_alarms[config['score_exponential']] = 0
number_of_alarms[config['score_transition_probability']] = 0
number_of_alarms[config['score_frequency']] = 0
number_of_alarms[config['score_type']] = 0

for i in range(len(number_of_alarms)):
    type= number_of_alarms.loc[i, config['type']]
    alarm_number= number_of_alarms.loc[i, config['number_of_alarms']]
    weighted_number = number_of_alarms.loc[i, config['weighted_number_of_alarms']]
    lamda = average_number_of_alarms.loc[average_number_of_alarms[config['type']] == type,config['average_weighed_number_alamrs']]
    number_of_alarms.loc[i, config['poisson_probability']] = poisson.pmf(weighted_number, mu=lamda)  # same as: (np.exp(-lam)*(lam**n))/math.factorial(n)
    number_of_alarms.loc[i, config['score_poisson']] = poisson.cdf(weighted_number, mu=lamda)  # same as: (np.exp(-lam)*(lam**n))/math.factorial(n)
    type_cell_interval = interval_alarms[(interval_alarms[config_interval['type']] == type) & (interval_alarms[config_interval['cell_id']] == number_of_alarms.loc[i, config['cell_id']]) & (interval_alarms[config['interval_number']] == number_of_alarms.loc[i, config['interval_number']])]
    type_cell_interval = type_cell_interval.reset_index(drop=True)
    if alarm_number > 1:
        time_average= type_cell_interval[config_interval['inter_arrival_time_min']].mean()
        mu = float(inter_arrival_time.loc[inter_arrival_time[config_interval['type']] == type,config['average_inter_arrival_time']])
        if mu == 0:
            number_of_alarms.loc[i, config['exponential_probability']] = 0
        else:
            number_of_alarms.loc[i, config['exponential_probability']] = expon.cdf(time_average,scale=mu)  # same as (1-np.exp(-1/mu*d.loc[j,'Inter-arrival time'])); https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.expon.html
        P_3 = []
        for j in range(0, len(type_cell_interval) - 1):
            description_1 = type_cell_interval.loc[j, config_interval['description']]
            description_2 = type_cell_interval.loc[j + 1, config_interval['description']]
            description_index_type = description_index[description_index[config['type']] == type]
            description_index_type = description_index_type.reset_index(drop=True)
            description_1_index = np.where(description_index_type[config['description']] == description_1)[0][0]
            description_2_index = np.where(description_index_type[config['description']] == description_2)[0][0]
            transition_matrix=pd.read_excel(os.path.join(config["data_directory"], config["data_name"]), sheet_name=type,index_col=config['index_col'])
            P_3.append(transition_matrix.iloc[description_1_index, description_2_index])
        number_of_alarms.loc[i, config['transition_probability']] = min(P_3)
    score_4 = []
    for k in range(len(type_cell_interval)):
        score_4.append(
            float(S4.loc[(S4[config['type']] == type_cell_interval.loc[k, config_interval['type']]) & (S4[config_interval['description']] == type_cell_interval.loc[k, config_interval['description']]), config['score_frequency']]))
    number_of_alarms.loc[i, config['score_frequency']] = max(score_4)

path_result = os.path.join(config["data_directory"], config["data_name"])
book = load_workbook(path_result)
writer_result = pd.ExcelWriter(path_result, engine='openpyxl')
writer_result.book = book

number_of_alarms.to_excel(writer_result, sheet_name=config['sheet_score_type'])
writer_result.save()
