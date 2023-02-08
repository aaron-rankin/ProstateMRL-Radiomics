import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
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
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\Delta_fts_pICC.csv")
fractions = df_all["Fraction"].unique()
fts = df_all["Feature"].unique()

df_res = pd.DataFrame()

# loop through all features
df_fr1 = df_all[df_all["Fraction"] == 1]
vals_vol1 = df_fr1[df_fr1["Feature"] == "original_shape_MeshVolume"]["FeatureValue"].values
for ft in fts:
    vals_ft1 = df_fr1[df_fr1["Feature"] == ft]["FeatureValue"].values
    rho = stats.spearmanr(vals_vol1, vals_ft1)[0]
    df_temp = pd.DataFrame({"Fraction": [1], "Feature": [ft], "rho": [rho]})
    df_res = df_res.append(df_temp)

df_fr2 = df_all[df_all["Fraction"].isin([4,5])]
vals_vol2 = df_fr2[df_fr2["Feature"] == "original_shape_MeshVolume"]["FeatureValue"].values

for ft in fts:
    vals_ft2 = df_fr2[df_fr2["Feature"] == ft]["FeatureValue"].values
    rho = stats.spearmanr(vals_vol2, vals_ft2)[0]
    df_temp = pd.DataFrame({"Fraction": [2], "Feature": [ft], "rho": [rho]})
    df_res = df_res.append(df_temp)

# calculate mean rho for each feature
df_mean = df_res.groupby("Feature").mean().reset_index()
fts_remove = df_mean[abs(df_mean["rho"]) > 0.6]["Feature"].values
df_all = df_all[~df_all["Feature"].isin(fts_remove)]
fts_remove = pd.DataFrame({"Feature": fts_remove})

print(fts_remove)
fts_remove.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\Delta_fts_remove_Volume.csv", index=False)

# save to csv
df_all.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\Delta_fts_pVol.csv", index=False)