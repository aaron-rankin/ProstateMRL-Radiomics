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

# load in limbus data Limbus key
df_key = pd.read_csv(root + "Aaron\ProstateMRL\Code\Extraction\PatKeys\LimbusKey_s.csv")

# load in patient data
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Limbus\Limbus_fts_all.csv")

# filter only SABR patients
patIDs = UF.SABRPats()[0:10] 
df_key = df_key[df_key["Treatment"] == "SABR"]
df_key = df_key[df_key["PatID"].isin(patIDs)]

# merge with limbus key, only want Days Column
df_all = pd.merge(df_all, df_key[["PatID", "Scan", "Days", "Fraction"]], on = ["PatID", "Scan"], how = "left")
# loop through all patients
df_final = pd.DataFrame()

df_all = df_all.drop(columns = [col for col in df_all.columns if "diagnostics" in col])
df_all = df_all.drop(columns = [col for col in df_all.columns if "Unnamed" in col])

df_res = pd.DataFrame()

fts = df_all.columns[3:-1]

# loop through days
days = df_all["Days"].unique()
fractions = df_all["Fraction"].unique()
for fr in fractions:
    df_fr = df_all[df_all["Fraction"] == fr]
    df_fr = df_fr.drop(columns = ["Scan", "Days", "Fraction"])

    # pivot df_day so that id is mask and variable is feature
    df_fts = df_fr.melt(id_vars = ["Mask", "PatID"], var_name = "variable", value_name = "value")

    fts = df_fts["variable"].unique()
    for ft in tqdm(fts):
        df_ft = df_fts[df_fts["variable"] == ft]
        icc = pg.intraclass_corr(data = df_ft, targets = "PatID", raters = "Mask", ratings = "value")
        df_res_t = pd.DataFrame()
        df_res_t = df_res_t.append(icc)

        # insert day and feature
        df_res_t["Fraction"] = int(fr)
        df_res_t["Feature"] = ft
        df_res = df_res.append(df_res_t)

# only want ICC3 
df_res = df_res[df_res["Type"] == "ICC3"]
df_res = df_res.drop(columns = ["Type", "Description"])

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
df_all = df_all.drop(columns = fts_remove)
fts_remove = pd.DataFrame(fts_remove, columns = ["Feature"])
fts_remove.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Limbus\ICC_fts_remove.csv", index = False)

# pivot df_all so that id is mask and variable is feature
#df_all_r = df_all.melt(id_vars = ["Mask", "PatID", "Days", "Fraction", "Scan"], var_name = "Feature", value_name = "FeatureValue")
#df_all_r["Fraction"] = df_all_r["Fraction"].astype(int)

# save df_all_r
#df_all_r.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Limbus\Limbus_fts_pICC.csv", index = False)