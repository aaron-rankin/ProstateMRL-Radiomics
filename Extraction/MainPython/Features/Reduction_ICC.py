import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pingouin as pg
from scipy import stats

import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(2)

# load in limbus data Limbus key
df_key = pd.read_csv(root + "Aaron\ProstateMRL\Code\Extraction\PatKeys\LimbusKey_s.csv")

# load in patient data
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Limbus\Limbus_fts.csv")

# filter only SABR patients
patIDs = UF.SABRPats()[0:10] 
df_key = df_key[df_key["Treatment"] == "SABR"]
df_key = df_key[df_key["PatID"].isin(patIDs)]

# merge with limbus key, only want Days Column
df_all = pd.merge(df_all, df_key[["PatID", "Scan", "Days"]], on = ["PatID", "Scan"], how = "left")
# loop through all patients
df_final = pd.DataFrame()

for pat in patIDs:
    df_pat = df_all[df_all["PatID"].isin([pat])]

    # drop all columns with Diagnostic in name
    df_pat = df_pat.drop(columns = [col for col in df_pat.columns if "diagnostics" in col])
    df_pat = df_pat.drop(columns = [col for col in df_pat.columns if "Unnamed" in col])

    # df_m = df_pat[df_pat["Mask"] == "RP"]
    # df_l = df_pat[df_pat["Mask"] == "Limbus"]
    # # drop mask column
    # df_m = df_m.drop(columns = ["Mask"])
    # df_l = df_l.drop(columns = ["Mask"])

    df_res = pd.DataFrame()

    fts = df_pat.columns[3:-1]
    
    # loop through days
    days = df_pat["Days"].unique()
    for day in days:
        df_day = df_pat[df_pat["Days"] == day]
        print(df_day)
        df_day = df_day.drop(columns = ["PatID", "Scan", "Days"])
        print(df_day)

        # pivot df_day so that id is mask and variable is feature
        df_ft = df_day.melt(id_vars = ["Mask"], var_name = "variable", value_name = "value")

        print(df_ft)

        fts = df_ft["variable"].unique()
        for ft in fts:
            df_ft = df_ft[df_ft["variable"] == ft]
            icc = pg.intraclass_corr(data = df_ft, targets = "variable", raters = "mask", ratings = "value")
            print(icc)
            df_res = df_res.append(icc)



        # for ft in fts:
        #     df_ft = df_pat[["PatID", "Days", "Mask", ft]]
        #     # Pivot table
        #     print(df_ft)
        #     print(df_ft)

        #     # get ICC
        #     icc = pg.intraclass_corr(data = df_ft, targets = "variable", raters = "mask", ratings = "value")
        #     fts_m = df_m[ft]
        #     fts_l = df_l[ft]

        #     print(pat, ft)
        # get ICC

    