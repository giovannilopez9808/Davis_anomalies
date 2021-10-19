import pandas as pd
import os


def join_headers(data: pd.DataFrame):
    columns = []
    for column in data.columns:
        space = " "
        text1 = column.split(".")[0]
        text1 = text1.replace(" ", "")
        text2 = data[column][0]
        text2 = text2.replace(" ", "")
        if("Unnamed" in column):
            text1 = ""
            space = ""
        columns.append(text1+space+text2)
    return columns


def format_date(data: pd.DataFrame):
    data["date"] = "0"
    for index in data.index:
        date = data["Date"][index].split("/")
        data["date"][index] = "20"+date[2]+"-"+date[1]+"-"+date[0]
    data.index = pd.to_datetime(data["date"])
    data = data.drop(["date", "Date"], 1)
    return data


def format_data(data: pd.DataFrame):
    columns = data.columns
    for column in columns:
        data[column] = data[column].replace("---", "")
    return data


pd.options.mode.chained_assignment = None
parameters = {"path data": "../Data/Davis/",
              "path results": "../Data/"}
files = sorted(os.listdir(parameters["path data"]))
for file in files:
    print("Analizando "+file)
    headers = pd.read_csv("{}{}".format(parameters["path data"],
                                        file),
                          sep="\t",
                          nrows=1,
                          low_memory=False)
    data = pd.read_csv("{}{}".format(parameters["path data"],
                                     file),
                       sep="\t",
                       skiprows=1,
                       low_memory=False)
    columns = join_headers(headers)
    data.columns = columns
    data = format_date(data)
    data = format_data(data)
    data.to_csv("{}{}".format(parameters["path results"],
                              file.replace("txt", "csv")))
