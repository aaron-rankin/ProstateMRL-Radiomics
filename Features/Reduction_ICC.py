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

# load in patient data
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHMFSTP\Limbus_fts_change.csv")

fractions = df_all["Fraction"].unique()
for fr in fractions:
    df_fr = df_all[df_all["Fraction"] == fr]


    fts = df_fr["Feature"].unique()
    df_res = pd.DataFrame()
    for ft in tqdm(fts):
        df_ft = df_fr[df_fr["Feature"] == ft]
        icc = pg.intraclass_corr(data = df_ft, targets = "PatID", raters = "Mask", ratings = "FeatureValue")
        df_res_t = pd.DataFrame()
        df_res_t = df_res_t.append(icc)

        # insert day and feature
        df_res_t["Fraction"] = int(fr)
        df_res_t["Feature"] = ft
        df_res = df_res.append(df_res_t)

# only want ICC3 
df_res = df_res[df_res["Type"] == "ICC2"]
df_res = df_res.drop(columns = ["Type", "Description"])
print(df_res)

# convert icc to float
df_res["ICC"] = df_res["ICC"].astype(float)
# loop through each row and classify ICC val
df_res["ICC_Class"] = df_res["ICC"].apply(lambda x: "Poor" if x < 0.5 else "Moderate" if x < 0.75 else "Good" if x < 0.9 else "Excellent")

# get average ICC for each feature over all fractions
df_res = df_res.groupby(["Feature", "ICC_Class"]).mean().reset_index()

# return rows with poor ICC
df_poor = df_res[df_res["ICC_Class"] == "Poor"]
fts_remove = df_poor["Feature"].unique()

# remove poor features from df_all
df_all = df_all[~df_all["Feature"].isin(fts_remove)]
fts_remove = pd.DataFrame(fts_remove, columns = ["Feature"])
print(fts_remove)
fts_remove.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHMFSTP\\fts_remove_ICC.csv", index = False)

# read in all features
df_all_r = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHMFSTP\\All_fts_change.csv")
df_all_r = df_all_r[~df_all_r["Feature"].isin(fts_remove["Feature"])]

# save df_all_r
df_all_r.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHMFSTP\\All_fts_pICC.csv", index = False)