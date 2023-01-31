import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd
import pingouin as pg
from scipy import stats
from tqdm import tqdm
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(2)

# read in fts from csv
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Limbus\All_fts_pVol.csv")

patIDs = df_all["PatID"].unique()
fts = df_all["Feature"].unique()

df_out = pd.DataFrame()
# loop through patients
for pat in patIDs:
    df_pat = df_all[df_all["PatID"] == pat]

    # loop through fts
    for ft in fts:
        vals_ft = df_pat[df_pat["Feature"] == ft]["FeatureValue"].values
        # calculate change in feature value from fraction 1
        df_pat.loc[df_pat["Feature"] == ft, "FeatureChange"] = (vals_ft - vals_ft[0]) / vals_ft[0]

    df_out = df_out.append(df_pat)

df_out.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Limbus\All_fts_change.csv", index=False)