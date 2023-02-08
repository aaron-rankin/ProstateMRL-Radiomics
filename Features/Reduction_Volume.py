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
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\All_fts_pICC.csv")
fractions = df_all["Fraction"].unique()
fts = df_all["Feature"].unique()

df_res = pd.DataFrame()

for fr in fractions:
    df_fr = df_all[df_all["Fraction"] == fr]
    df_vol = df_fr[df_fr["Feature"] == "original_shape_MeshVolume"]
    vals_vol = df_vol["FeatureValue"].values

    # loop through features
    for ft in fts:
        # correlate to volume
        df_ft = df_fr[df_fr["Feature"] == ft]
        vals_ft = df_ft["FeatureValue"].values

        # get spearman correlation
        rho = stats.spearmanr(vals_vol, vals_ft)[0]

        df_temp = pd.DataFrame({"Fraction": [fr], "Feature": [ft], "rho": [rho]})
        df_res = df_res.append(df_temp)


# calculate mean rho for each feature
df_mean = df_res.groupby("Feature").mean().reset_index()
# remove features
fts_remove = df_mean[abs(df_mean["rho"]) > 0.6]["Feature"].values
df_all = df_all[~df_all["Feature"].isin(fts_remove)]
fts_remove = pd.DataFrame({"Feature": fts_remove})
print(fts_remove)
fts_remove.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\fts_remove_Volume.csv", index=False)

# save to csv
df_all.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\All_fts_pVol.csv", index=False)

    