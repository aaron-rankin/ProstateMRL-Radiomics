import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
from datetime import datetime
import radiomics
from radiomics import featureextractor
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(1)
# Patient Key
patKey = pd.read_csv(root + "\\Aaron\\ProstateMRL\\Code\\Extraction\\PatKeys\\LimbusKey.csv")
niftiDir = root + "prostateMR_radiomics\\nifti\\"
outDir = root + "Aaron\\ProstateMRL\\Data\\Pipeline_v2\\FeatureValues\\"

# filter only SABR patients
patKey = patKey[patKey["Treatment"] == "SABR"]

# loop through all patients
patIDs = UF.SABRPats()
results_df = pd.DataFrame()

extractor_params = root + "Aaron\\ProstateMRL\\Data\\MRLPacks\\ExtractionParams\\All.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(extractor_params)

for pat in patIDs:
    p_df = patKey[patKey["PatID"].isin([pat])]
    p_vals = pd.DataFrame(columns=["PatID", "Scan", "Mask"])
    # get file directory for patient
    patDir = p_df["Directory"].values[0]

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
        Limbus_mask = scanDir + "Masks\\" +  pat + "_" + scan + "_Limbus_shrunk.nii"
        masks = [RP_mask, Limbus_mask]

        for m in masks:
            # get the mask name
            if m == RP_mask:
                maskName = "RP"
            else:
                maskName = "Limbus"
            # create a new row for the dataframe
            new_row = {"PatID": pat, "Scan": scan, "Mask": maskName}

            feat_df = pd.DataFrame()
            # extract features
            temp_results = pd.Series(extractor.execute(imgFile, m, label=255))
            feat_df = feat_df.append(temp_results, ignore_index=True)
            # merge new row with feature dataframe with new row first
            feat_df = pd.concat([pd.DataFrame(new_row, index=[0]), feat_df], axis=1)
            # append to the patient dataframe
            p_vals = p_vals.append(feat_df, ignore_index=True)

    # append to the results dataframe
    results_df = results_df.append(p_vals, ignore_index=True)

# save the results
results_df.to_csv(outDir + "Limbus_fts.csv")


