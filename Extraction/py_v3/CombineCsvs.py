import os 
import pandas as pd

url = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Features_v3\\"

csvs = os.listdir(url)

all_df = pd.DataFrame()

for i in csvs:
    temp = pd.read_csv(url + i)
    all_df = all_df.append(temp)

all_df.to_csv(url + "All_FOSh.csv")
