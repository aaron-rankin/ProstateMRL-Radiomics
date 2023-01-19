import pandas as pd
import numpy as np
import UsefulFunctions as UF
dir_in = 'D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\VolIndFts\\'
dir_out = 'D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DeltaTrial\\DeltaVals\\'

Norms = UF.NormArray()
patIDs = UF.SABRPats()

for n in Norms:
    df_n = pd.read_csv(dir_in + n + ".csv")
    
    df_n["PatID"] = df_n["PatID"].astype(str)
    df_out = pd.DataFrame()
    for p in patIDs:
       # print(p)
        df_p = df_n[df_n["PatID"] == str(p)]
        #print(df_p)
        timepoints = df_p["DaysDiff"].unique()
        #print(timepoints)
        times = [timepoints[0], timepoints[-1]]
        #df_temp = df_p[df_p["DaysDiff"].isin(times)]
        df_temp = df_p[df_p["DaysDiff"] == timepoints[-1]]
        #print(df_temp)
        df_out = df_out.append(df_temp, ignore_index=True)

    df_out = df_out[["PatID", "DaysDiff",  "Normalisation", "FeatureName", "FeatureChange"]]
    df_out.to_csv(dir_out + n + ".csv")
