import numpy as np
import pandas as pd
import os

# IF Change csvs
url_if = "D:\\data\\Aaron\\ProstateMRL\\Data\MRLPacks\\InterFractionChanges\\"
if_dir = os.listdir(url_if)

# Read in feature csvs
url_ft = "D:\\data\\Aaron\\ProstateMRL\\Data\MRLPacks\\FeatureExtraction\\"
ft_dir = os.listdir(url_ft)

output_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\MRLPacks\\FeatureChange\\"


for i in ft_dir:
    patID = str(i)
    ifc_df = pd.read_csv(url_if + patID + "_inter.csv")
    ifc_df = ifc_df.loc[ifc_df["Region"] == "Prostate"]
    fractions = ifc_df.Fraction.unique()
    norms = ifc_df.Normalisation.unique()

    pat_folder = output_dir + patID
    if os.path.exists(pat_folder):	
        print()
    else:
        os.mkdir(pat_folder)

    for n in norms:
        norm = n
        norm_df = ifc_df.loc[ifc_df["Normalisation"] == norm]

        final_df = pd.DataFrame()

        for j in fractions:
            fraction = j
            frac_df = norm_df.loc[ifc_df["Fraction"] == fraction]
            MR = frac_df.iloc[0]["MRContour"]

            print("Patient: {} | Fraction: {} | MRContour: {} | Normalisation: {}".format(patID, fraction, MR, norm))

            ft_df = pd.read_csv(url_ft + patID + "\\" + MR + "\\" + patID + "_" + MR + "_" + norm + "_features.csv")

            r_df = frac_df[["Fraction", "DaysDiff"]].copy()
            ft_df = ft_df.iloc[:, 23:]
            r_df.reset_index(drop=True, inplace=True)
            ft_df.reset_index(drop=True, inplace=True)
            res_df = pd.concat([r_df, ft_df], axis=1, join="outer")
            
            if fraction == fractions.min():
                ff_df = res_df
            
            change_df = (res_df.iloc[:, 23:] - ff_df.iloc[:, 23:]) / ff_df.iloc[:, 23:]
            change_df.rename(columns=lambda x: "change_" + x, inplace=True)
            change_df.reset_index(drop=True, inplace=True)
            res_df = pd.concat([res_df, change_df], axis=1, join="outer")

            final_df = final_df.append(res_df)

        final_df = final_df.T
        final_df.to_csv(pat_folder + "\\" + patID + "_" + norm + "_ft_changes.csv")
