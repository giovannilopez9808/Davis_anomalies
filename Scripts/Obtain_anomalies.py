import pandas as pd
import os


def read_data(path: str, file: str):
    data = pd.read_csv("{}{}".format(path,
                                     file),
                       index_col=0,
                       low_memory=False)
    data.index = pd.to_datetime(data.index)
    return data


def clean_data(data: pd.DataFrame, variables: list):
    columns = data.columns
    columns = columns.drop(variables)
    data = data.drop(columns, 1)
    for variable in variables:
        data[variable] = data[variable].astype(float)
    return data


def obtain_mean(data: pd.DataFrame):
    year = data.index[0].year
    date_inital = "{}-06-01".format(year)
    date_final = "{}-08-31".format(year)
    data = data[data.index >= date_inital]
    data = data[data.index <= date_final]
    mean = data.mean()
    return mean


parameters = {"path data": "../Data/",
              "variables": ["Temp Out", "Out Hum", "Rain"],
              "year initial": 2010,
              "year final": 2020,
              "date initial": "2010"}

files = sorted(os.listdir(parameters["path data"]))
files = [file for file in files if ".csv" in file]
years = [year for year in range(parameters["year initial"],
                                parameters["year final"]+1)]
mean = pd.DataFrame(index=years,
                    columns=parameters["variables"])
for file in files:
    data_per_file = read_data(parameters["path data"],
                              file)
    data_per_file = clean_data(data_per_file, parameters["variables"])
    mean_per_file = obtain_mean(data_per_file)
    year = data_per_file.index[0].year
    for variable in parameters["variables"]:
        mean[variable][year] = mean_per_file[variable]
mean_period = mean[mean.index >= 2010]
mean_period = mean_period[mean_period <= 2019]
mean_period = mean_period.mean()
mean_year = mean[mean.index == 2020]
for variable in parameters["variables"]:
    diff = mean_year[variable]-mean_period[variable]
    print("{}:\t{}".format(variable, round(list(diff)[0], 6)))
