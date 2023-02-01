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

df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Features\All_fts_change.csv")
PatIDs = df_all["PatID"].unique()
fts = df_all["Feature"].unique()

df_out = pd.DataFrame()

# loop through all patients
for pat in PatIDs:
    df_pat = df_all[df_all["PatID"] == pat]
    f1,f2 = df_pat["Fraction"].values[0], df_pat["Fraction"].values[-1]
    df_pat = df_pat[df_pat["Fraction"].isin([f1,f2])]
    
    df_out = df_out.append(df_pat)

df_out.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Features\delta_fts_all.csv", index = False)


df_lim = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Features\Limbus_fts_change.csv")
PatIDs = df_lim["PatID"].unique()
fts = df_lim["Feature"].unique()

df_out = pd.DataFrame()

# loop through all patients
for pat in PatIDs:
    df_pat = df_lim[df_lim["PatID"] == pat]
  
    f1,f2 = df_pat["Fraction"].values[0], df_pat["Fraction"].values[-1]
    df_pat = df_pat[df_pat["Fraction"].isin([f1,f2])]
    
    df_out = df_out.append(df_pat)

df_out.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Features\delta_fts_limbus.csv", index = False)