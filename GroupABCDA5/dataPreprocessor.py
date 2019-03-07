import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import json
from datetime import datetime,date
import warnings
warnings.filterwarnings("ignore")

def preprocessor():
    df = pd.read_csv("mtadata.csv")
    list1 = []
    list2_3 = []
    for i, row in df.iterrows():
        if row["routeId"] in ["1", "2", "3"]:
            dict_futureStopData = json.loads(row["futureStopData"])
            if "127S" in dict_futureStopData and "120S" in dict_futureStopData and row["vehicleTimeStamp"] is not " ":
                entry = {
                    "96_time": dict_futureStopData["127S"]["arrivalTime"],
                    "42_time": dict_futureStopData["120S"]["arrivalTime"],
                    "weekday": time.strftime('%A',time.localtime(int(row["vehicleTimeStamp"]))) 
                }
                if row["routeId"] is "1":
                    list1.append(entry)
                if row["routeId"] in ["2", "3"]:
                    list2_3.append(entry)  
    print("list1:")
    print(list1)
    print("list2_3:")
    print(list2_3)
    
if __name__ == "__main__":
    preprocessor()