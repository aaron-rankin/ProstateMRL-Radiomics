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
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\Delta_fts_limbus.csv")

fts = df_all["Feature"].unique()
fractions = df_all["Fraction"].unique()

df_res = pd.DataFrame()

# loop through all features
df_fr1 = df_all[df_all["Fraction"] == 1]

for ft in fts:
    df_ft = df_fr1[df_fr1["Feature"] == ft]
    df_res_t = pd.DataFrame()
    icc = pg.intraclass_corr(data = df_ft, targets = "PatID", raters = "Mask", ratings = "FeatureValue")
    df_res_t = df_res_t.append(icc)
    df_res_t["Feature"] = ft

    df_res = df_res.append(df_res_t)

df_fr5 = df_all[df_all["Fraction"].isin([4,5])]
for ft in fts:
    df_ft = df_fr5[df_fr5["Feature"] == ft]
    df_res_t = pd.DataFrame()
    icc = pg.intraclass_corr(data = df_ft, targets = "PatID", raters = "Mask", ratings = "FeatureValue")
    df_res_t = df_res_t.append(icc)
    df_res_t["Feature"] = ft

    df_res = df_res.append(df_res_t)


df_res = df_res[df_res["Type"] == "ICC2"]
df_res = df_res.drop(columns = ["Type", "CI95%", "Description"])

# convert icc to float
df_res["ICC"] = df_res["ICC"].astype(float)
# loop through each row and classify ICC val
df_res["ICC_Class"] = df_res["ICC"].apply(lambda x: "Poor" if x < 0.5 else "Moderate" if x < 0.75 else "Good" if x < 0.9 else "Excellent")

# get average ICC for each feature over all fractions
df_res = df_res.groupby(["Feature", "ICC_Class"]).mean().reset_index()

df_poor = df_res[df_res["ICC_Class"] == "Poor"]
fts_remove = df_poor["Feature"].unique()

# remove poor features from df_all
df_all = df_all[~df_all["Feature"].isin(fts_remove)]
fts_remove = pd.DataFrame(fts_remove, columns = ["Feature"])
print(fts_remove)
fts_remove.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\Delta_fts_remove_ICC.csv", index = False)

# read in all features
df_all_r = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\Delta_fts_all.csv")
df_all_r = df_all_r[~df_all_r["Feature"].isin(fts_remove["Feature"])]

# save df_all_r
df_all_r.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\\Delta_fts_pICC.csv", index = False)
    