import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pingouin as pg
from scipy import stats
from tqdm import tqdm
import sys


def ICC(DataRoot, Norm, Model, output=False):
    root = DataRoot
    # load in patient data
    df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\" + Model + "_Limbus_fts.csv")
    # remove rows with original_firstorder_Minimum/Maximum
    df_all = df_all[df_all["Feature"] != "original_firstorder_Minimum"]
    df_all = df_all[df_all["Feature"] != "original_firstorder_Maximum"]

    if Model == "Longitudinal":
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

    elif Model == "Delta":
        df_all = df_all[df_all["Fraction"] != 1]
        fts = df_all["Feature"].unique()
        df_res = pd.DataFrame()
        for ft in tqdm(fts):
            df_ft = df_all[df_all["Feature"] == ft]
            icc = pg.intraclass_corr(data = df_ft, targets = "PatID", raters = "Mask", ratings = "FeatureChange")
            df_res_t = pd.DataFrame()
            df_res_t = df_res_t.append(icc)

            # insert day and feature
            df_res_t["Fraction"] = "Delta"
            df_res_t["Feature"] = ft
            df_res = df_res.append(df_res_t)

    # only want ICC3 
    df_res = df_res[df_res["Type"] == "ICC2"]
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
    if output == True:
        print("\nICC redudant features: " + str(len(fts_remove)) + "/" + str(len(fts)))
        # print features to remove one by one

        for ft in fts_remove:
            print(ft)

    # remove poor features from df_all
    df_all = df_all[~df_all["Feature"].isin(fts_remove)]
    # add original_firstorder_Minimum/Maximum to fts_remove
    fts_remove = np.append(fts_remove, "original_firstorder_Minimum")
    fts_remove = np.append(fts_remove, "original_firstorder_Maximum")
    fts_remove = pd.DataFrame(fts_remove, columns = ["Feature"])
    fts_remove.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\" + Model + "_FeaturesRemoved_ICC.csv", index = False)

    # read in all features
    df_all_r = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\" + Model + "_All_fts.csv")
    df_all_r = df_all_r[~df_all_r["Feature"].isin(fts_remove["Feature"])]

    # save df_all_r
    df_all_r.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\" + Model + "_fts_pICC.csv", index = False)



def Volume(DataRoot, Norm, Model, output = False):

    root = DataRoot
     # read in fts from csv
    df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\" + Model + "_fts_pICC.csv")
    fractions = df_all["Fraction"].unique()
    fts = df_all["Feature"].unique()

    df_res = pd.DataFrame()

    if Model == "Longitudinal":
        for fr in fractions:
            df_fr = df_all[df_all["Fraction"] == fr]
            df_vol = df_fr[df_fr["Feature"] == "original_shape_MeshVolume"]
            vals_vol = df_vol["FeatureValue"].values

            # loop through features
            for ft in tqdm(fts):
                # correlate to volume
                df_ft = df_fr[df_fr["Feature"] == ft]
                vals_ft = df_ft["FeatureValue"].values

                # get spearman correlation
                rho = stats.spearmanr(vals_vol, vals_ft)[0]

                df_temp = pd.DataFrame({"Fraction": [fr], "Feature": [ft], "rho": [rho]})
                df_res = df_res.append(df_temp)

    elif Model == "Delta":
        df_all = df_all[df_all["Fraction"] != 1]
        
        df_vol = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Delta_All_fts.csv")
        df_vol = df_vol[df_vol["Feature"] == "original_shape_MeshVolume"]
        df_vol = df_vol[df_vol["Fraction"] != 1]
        vals_vol = df_vol["FeatureValue"].values
        


        # loop through features
        for ft in tqdm(fts):
            df_ft = df_all[df_all["Feature"] == ft]
            vals_ft = df_ft["FeatureValue"].values

            # get spearman correlation
            rho = stats.spearmanr(vals_vol, vals_ft)[0]

            df_temp = pd.DataFrame({"Fraction": ["Delta"], "Feature": [ft], "rho": [rho]})
            df_res = df_res.append(df_temp)


    # calculate mean rho for each feature
    df_mean = df_res.groupby("Feature").mean().reset_index()
    # remove features
    fts_remove = df_mean[abs(df_mean["rho"]) > 0.6]["Feature"].values
    df_all = df_all[~df_all["Feature"].isin(fts_remove)]
    if output == True:
        print("\nVolume redundant features: " + str(len(fts_remove)) + "/" + str(len(fts)) )

        for ft in fts_remove:
            print(ft)

        print("Remaining features: " + str(len(df_all["Feature"].unique())) + "/" + str(len(fts)) + "\n")

    fts_remove = pd.DataFrame({"Feature": fts_remove})
    fts_remove.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\" + Model + "_FeaturesRemoved_Volume.csv", index=False)

    # save to csv
    df_all.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\" + Model + "_fts_pVol.csv", index=False)

        