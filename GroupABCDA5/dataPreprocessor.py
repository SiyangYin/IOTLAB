import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import json
from datetime import datetime,date
import warnings
warnings.filterwarnings("ignore")

def f(x):
    if x is not ' ':
        return time.strftime('%A',time.localtime(int(x)))
    else:
        return x

def preprocessor():
    df = pd.read_csv("mtadata.csv")
    df_96 = df[df["currentStopId (S)"] == "127S"]
    df_42 = df[df["currentStopId (S)"] == "120S"]
    list1 = []
    list2_3 = []
    for i, row in df.iterrows():
        if row["routeId (S)"] in ["1", "2", "3"]:
            dict_futureStopData = json.loads(row["futureStopData (M)"])
            if "127S" in dict_futureStopData and "120S" in dict_futureStopData and row["vehicleTimeStamp (N)"] is not " ":
                entry = {
                    "96_time": dict_futureStopData["127S"]["M"]["arrivalTime"]["N"],
                    "42_time": dict_futureStopData["120S"]["M"]["arrivalTime"]["N"],
                    "weekday": time.strftime('%A',time.localtime(int(row["vehicleTimeStamp (N)"]))) 
                }
                if row["routeId (S)"] is "1":
                    list1.append(entry)
                if row["routeId (S)"] in ["2", "3"]:
                    list2_3.append(entry)  
    print("list1:")
    print(list1)
    print("list2_3:")
    print(list2_3)
    
if __name__ == "__main__":
    preprocessor()