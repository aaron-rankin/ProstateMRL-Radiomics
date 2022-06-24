'''
Loop through patient directory with patients who have reg/normalised images
Load in first image at each fraction - need to load in scaninfo csv and find image
6 images - raw, Norm-Pros/Glute/Psoas, HM-TP/FS
3 masks - Prostate, Glute, Psoas
Calc mean signal and std

Output to csv:
PatID | Fraction | Contour | Date | Normalisation | Region | Mean Signal | Std Signal | d-Days | d-Mean Signal |

'''

import SimpleITK as sitk
from importlib_metadata import re
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys
#import seaborn as sns
import pandas as pd
import radiomics
import UsefulFunctions as UF
from datetime import datetime


# get packIDs and scaninfo directory
scaninfo_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\ScanInfo\\"
packedIDs = os.listdir(scaninfo_dir)

for p in range(len(packedIDs)):
    q = packedIDs[p]
    packedIDs[p] = q[:-4]

output_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges\\"
col_names = ["PatID","Treatment","Fraction","Date","MRContour","Normalisation","Region","MeanSignal", "StdSignal","DaysDiff","MeanDiff", "StdDiff"]
all_df = pd.DataFrame(columns=col_names)

# set patient directory
url_SABR = "D:\\data\\prostateMR_radiomics\\nifti\\SABR\\"
url_20f = "D:\\data\\prostateMR_radiomics\\nifti\\20fractions\\"

url = url_SABR

ptDir = os.listdir(url)

vals_scan = {}

# loop through ptDir if in packedIDs
for i in ptDir:
    if i in packedIDs:
        
        # load in pat scan info
        scaninfo = pd.read_csv(scaninfo_dir + i + ".csv")
        fractions = scaninfo.Fraction.unique()

        patID = i
        treatment = url.split("\\")[4]

        pat_df = pd.DataFrame(columns=col_names)

        # need to loop through fractions
        for j in fractions:
            frac = j

            frac_df = scaninfo.loc[scaninfo["Fraction"] == frac] 

            MRcont, scan_date = frac_df.iloc[0]["MRContour"], frac_df.iloc[0]["ScanDate"]
            MRcont, scan_date = MRcont[1:], (datetime.strptime(str(scan_date), "%Y%m%d")).date()

            print("Patient: {} Fraction: {} Contour: {}".format(patID, frac, MRcont))
            print("---------------------------------------------------------")
            
            # Generate paths
            pat_path = os.path.join(url, patID, MRcont)

            mask_path = os.path.join(pat_path, "Masks\\")
            masks = ["_shrunk_pros.nii", "_glute.nii", "_psoas.nii"]
            
            raw_path = os.path.join(pat_path, "Reg-Raw\\")
            norm_pros_path = os.path.join(pat_path, "Norm-Pros\\")
            norm_psoas_path = os.path.join(pat_path, "Norm-Psoas\\")
            norm_glute_path = os.path.join(pat_path, "Norm-Glute\\")
            HM_TP_path = os.path.join(pat_path, "HM-TP\\")
            HM_FS_path = os.path.join(pat_path, "HM-FS\\")

            image_paths = [raw_path, norm_glute_path, norm_pros_path, norm_psoas_path, HM_FS_path, HM_TP_path]
            
            for k in image_paths:
                images = os.listdir(k)

                # folder empty if haven't done norm
                if len(images) != 0:

                    # only want first scan (inter-fraction changes)
                    image_name = images[0]
                    image_url = os.path.join(k,image_name)

                    # loop through masks
                    for m in masks:
                        
                        mask_name = patID + "_" + MRcont + m
                        mask_url = os.path.join(mask_path, mask_name)
                        
                        norm, region = UF.GetNorm(image_name), UF.GetRegion(mask_name)
                        scan_mean, scan_std = UF.MaskedMeanStd(image_url, mask_url)

                        # get fraction 1 values

                        if frac == fractions[0]:
                            frac1_df = pd.DataFrame()
                            frac1_date = scan_date
                            frac1_mean, frac1_std = scan_mean, scan_std 
                            diff_days, diff_mean, diff_std = 0, 0, 0

                        # calc change
                        else:
                            diff_days = UF.DateDifference(frac1_date, scan_date)
                            diff_mean = scan_mean - pat_df[(pat_df["Region"] == region) & (pat_df["Normalisation"] == norm) & (pat_df["Fraction"] == int(fractions[0]))]["MeanSignal"].iloc[0]                      
                            diff_std = scan_std - pat_df[(pat_df["Region"] == region) & (pat_df["Normalisation"] == norm) & (pat_df["Fraction"] == int(fractions[0]))]["StdSignal"].iloc[0]

                        # append all values to dict
                        vals_scan["PatID"], vals_scan["Treatment"], vals_scan["Fraction"] = patID, treatment, int(frac)
                        vals_scan["MRContour"], vals_scan["Date"], vals_scan["Normalisation"] = MRcont, scan_date, norm
                        vals_scan["Region"], vals_scan["MeanSignal"], vals_scan["StdSignal"] = region, scan_mean, scan_std
                        vals_scan["DaysDiff"], vals_scan["MeanDiff"], vals_scan["StdDiff"] = diff_days, diff_mean, diff_std
                        pat_df = pat_df.append(vals_scan, ignore_index=True)
         
        pat_df.to_csv(output_dir + patID + ".csv")
        all_df = all_df.append(pat_df, ignore_index=True)

all_df.to_csv(output_dir + treatment + "_all.csv")
print("Finished")
