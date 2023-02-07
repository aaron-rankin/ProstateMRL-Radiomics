import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
from datetime import datetime
import radiomics
from radiomics import featureextractor
import sys
from tqdm import tqdm

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(1)
# Patient Key
patKey = pd.read_csv(root + "Aaron\\ProstateMRL\\Code\\PatKeys\\AllPatientKey_s.csv")
niftiDir = root + "prostateMR_radiomics\\nifti\\"
outDir = root + "Aaron\\ProstateMRL\\Data\\Paper1\\FeaturesHM\\"

# filter only SABR patients
patKey = patKey[patKey["Treatment"] == "SABR"]

# loop through all patients
patIDs = UF.SABRPats()  
results_df = pd.DataFrame()


extractor_params = root + "Aaron\\ProstateMRL\\Data\\MRLPacks\\ExtractionParams\\All.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(extractor_params)

for pat in tqdm(patIDs):
    p_df = patKey[patKey["PatID"].isin([pat])]

    p_vals = pd.DataFrame(columns=["PatID", "Scan", "Fraction", "Days", "Mask"])
    # get file directory for patient
    patDir = p_df["FileDir"].values[0]

    # get scans
    scans = p_df["Scan"].values
    fractions = patKey["Fraction"].values
    days = patKey["Days"].values

    pat = UF.FixPatID(pat, patDir)       
    patDir = niftiDir + patDir + "\\" + pat + "\\"

    for j in range(len(scans)):
        scan = scans[j]
        frac = fractions[j]
        day = days[j]

        # get the scan directory
        scanDir = patDir + scan + "\\"

        # image file
        imgFile = scanDir + "HM-FS\\" + pat + "_" + scan + "_HM-FS.nii"

        # mask files
        RP_mask = scanDir + "Masks\\"  + pat + "_" + scan + "_shrunk_pros.nii"

        # create a new row for the dataframe
        new_row = {"PatID": pat, "Scan": scan, "Fraction": frac, "Days": day, "Mask": "RP"}

        feat_df = pd.DataFrame()
        # extract features
        temp_results = pd.Series(extractor.execute(imgFile, RP_mask, label=255))
        feat_df = feat_df.append(temp_results, ignore_index=True)
        # merge new row with feature dataframe with new row first
        feat_df = pd.concat([pd.DataFrame(new_row, index=[0]), feat_df], axis=1)
        # append to the patient dataframe
        p_vals = p_vals.append(feat_df, ignore_index=True)
   
    # append to the results dataframe
    results_df = results_df.append(p_vals, ignore_index=True)


# save the results and merge to patient key

results_df = results_df.drop(columns = [col for col in results_df.columns if "diagnostics" in col])
results_df = results_df.drop(columns = [col for col in results_df.columns if "Unnamed" in col])

results_df = results_df.sort_values(by = ["PatID", "Fraction", "Days"])

# save the results
results_df.to_csv(outDir + "All_fts.csv")

results_df = results_df.melt(id_vars = ["PatID", "Scan", "Days", "Fraction", "Mask"], var_name = "Feature", value_name = "FeatureValue")
fts = results_df["Feature"].unique()
PatIDs = results_df["PatID"].unique()
df_out = pd.DataFrame()
# loop through all patients
for pat in PatIDs:
    df_pat = results_df[results_df["PatID"].isin([pat])]
    df_pat = df_pat.sort_values(by = ["Days", "Fraction"])
    print(df_pat.head())
    # loop through all features
    for ft in fts:
        vals_ft = df_pat[df_pat["Feature"] == ft]["FeatureValue"].values
        if vals_ft[0] == 0:
            ft_change = np.zeros(len(vals_ft))
        else:
            ft_change = (vals_ft - vals_ft[0]) / vals_ft[0]
                    
        df_pat.loc[df_pat["Feature"] == ft, "FeatureChange"] = ft_change

    df_out = df_out.append(df_pat)

df_out.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\FeaturesHM\All_fts_change.csv", index=False)
