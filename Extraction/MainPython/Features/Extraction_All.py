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

root = UF.DataRoot(2)
# Patient Key
patKey = pd.read_csv(root + "\\Aaron\\ProstateMRL\\Code\\Extraction\\PatKeys\\AllPatientKey_s.csv")
niftiDir = root + "prostateMR_radiomics\\nifti\\"
outDir = root + "Aaron\\ProstateMRL\\Data\\Paper1\\Features\\"

# filter only SABR patients
patKey = patKey[patKey["Treatment"] == "SABR"]

# loop through all patients
patIDs = UF.SABRPats()  
results_df = pd.DataFrame()


extractor_params = root + "Aaron\\ProstateMRL\\Data\\MRLPacks\\ExtractionParams\\All.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(extractor_params)

for pat in tqdm(patIDs):
    p_df = patKey[patKey["PatID"].isin([pat])]
    p_vals = pd.DataFrame(columns=["PatID", "Scan", "Mask"])
    # get file directory for patient
    patDir = p_df["FileDir"].values[0]

    # get scans
    scans = p_df["Scan"].values

    pat = UF.FixPatID(pat, patDir)       
    patDir = niftiDir + patDir + "\\" + pat + "\\"

    print("-"*15)

    for scan in scans:
        print("{} - {}".format(pat, scan))

        # get the scan directory
        scanDir = patDir + scan + "\\"

        # image file
        imgFile = scanDir + "RawImages\\" + pat + "_" + scan + "_Raw.nii"

        # mask files
        RP_mask = scanDir + "Masks\\"  + pat + "_" + scan + "_shrunk_pros.nii"

        # create a new row for the dataframe
        new_row = {"PatID": pat, "Scan": scan}

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

PatKey = pd.read_csv(root + "\\Aaron\\ProstateMRL\\Code\\Extraction\\PatKeys\\AllPatientKey_s.csv")
PatKey = PatKey[PatKey["Treatment"] == "SABR"]

results_df = results_df.drop(columns = [col for col in results_df.columns if "diagnostics" in col])
results_df = results_df.drop(columns = [col for col in results_df.columns if "Unnamed" in col])

fts = results_df.columns[2:]

fractions = PatKey["Fraction"].unique()
patIDs = PatKey["PatID"].unique()

# merge with patient key to get date and days and fraction
results_df_m = pd.merge(results_df, PatKey[["PatID", "Scan", "Days", "Fraction"]],on = ["PatID", "Scan"], how = "left")

frac = results_df_m.pop("Fraction")
results_df_m.insert(2, "Fraction", frac)

days = results_df_m.pop("Days")
results_df_m.insert(3, "Days", days)

results_df_m["Days"] = results_df_m["Days"].astype(int)
results_df_m["Fraction"] = results_df_m["Fraction"].astype(int)

results_df_m = results_df_m.sort_values(by = ["PatID", "Fraction", "Days"])
# save the results
results_df_m.to_csv(outDir + "All_fts.csv")


