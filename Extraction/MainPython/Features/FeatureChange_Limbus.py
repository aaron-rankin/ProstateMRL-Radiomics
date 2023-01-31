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
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Features\Limbus_fts_all.csv")
df_key = pd.read_csv(root + "Aaron\ProstateMRL\Code\Extraction\PatKeys\LimbusKey_s.csv")
df_key = df_key[df_key["Treatment"] == "SABR"]

PatIDs = df_key["PatID"].unique()[0:10]
df_key = pd.read_csv(root + "Aaron\ProstateMRL\Code\Extraction\PatKeys\AllPatientKey_s.csv")
df_key = df_key[df_key["Treatment"] == "SABR"]
df_key = df_key[df_key["PatID"].isin(PatIDs)]

df_all = pd.merge(df_all, df_key[["PatID", "Scan", "Days", "Fraction"]], on = ["PatID", "Scan"], how = "left")

df_all["Days"] = df_all["Days"].astype(int)
df_all["Fraction"] = df_all["Fraction"].astype(int)
df_all = df_all.drop(columns = [col for col in df_all.columns if "diagnostics" in col])
df_all = df_all.drop(columns = [col for col in df_all.columns if "Unnamed" in col])

days = df_all.pop("Days")
fractions = df_all.pop("Fraction")

df_all.insert(3, "Days", days)
df_all.insert(4, "Fraction", fractions)

# pivot long so each row is feature and feature value
df_all = df_all.melt(id_vars = ["PatID", "Scan", "Mask", "Days", "Fraction"], var_name = "Feature", value_name = "FeatureValue")

fts = df_all["Feature"].unique()
masks = df_all["Mask"].unique()

df_out = pd.DataFrame()
# loop through all patients
for pat in PatIDs:
    df_pat = df_all[df_all["PatID"] == pat]
    df_pat = df_pat.sort_values(by = ["Days", "Fraction"])

    for m in masks:
        df_mask = df_pat[df_pat["Mask"] == m]

        # loop through all features
        for ft in fts:
            vals_ft = df_mask[df_mask["Feature"] == ft]["FeatureValue"].values
            if vals_ft[0] == 0:
                ft_change = np.zeros(len(vals_ft))
            else:
                ft_change = (vals_ft - vals_ft[0]) / vals_ft[0]
                        
            df_mask.loc[df_mask["Feature"] == ft, "FeatureChange"] = ft_change

        df_out = df_out.append(df_mask)

df_out.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Features\Limbus_fts_change.csv", index=False)
