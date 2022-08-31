'''
Read in matched images and mean values
Get mean signal of mask in frac 1 scan 1
Norm factor = frac1scan1 / fracxscanx
Multiply whole image by norm factor
'''

from tkinter import Label
import SimpleITK as sitk
from matplotlib.pyplot import contour
import numpy as np
import pandas as pd
import os
import UsefulFunctions as UF

root = UF.DataRoot()
url = root + "prostateMR_radiomics\\nifti\\"
# csv_url = "root\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges\\"
scans_df = pd.read_csv(root + "\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges_v3\\Base_signal_changes_pyRad.csv")
treatments = ["SABR"]  

url_SABR = root + "\\prostateMR_radiomics\\nifti\\SABR\\"
url_20f = root + "\\prostateMR_radiomics\\nifti\\20fractions\\"


for t in treatments:
    t_df = scans_df.loc[scans_df["Treatment"] == t]
    patIDs = t_df.PatID.unique()
    Regions = t_df.Region.unique()
    print(t)
    print(patIDs)
    #print(t_df.head())
    raw_df = t_df.loc[t_df["Normalisation"] == "Raw"]
    #print(raw_df.head())

    for i in patIDs:
        # read in pat csv
        pat_df = raw_df[raw_df["PatID"].isin([i])]
        print("-"*20)
        #print(i)
        
        
        base_df = pat_df.loc[pat_df["DaysDiff"]==0]
        #print(base_df.head())
        base_pros_mean, base_glute_mean, base_psoas_mean = base_df["Mean"].iloc[0], base_df["Mean"].iloc[1], base_df["Mean"].iloc[2]
        base_pros_med, base_glute_med, base_psoas_med = base_df["Median"].iloc[0], base_df["Median"].iloc[1], base_df["Median"].iloc[2]
        #print(base_pros_mean, base_glute_mean, base_psoas_mean)
        #print(base_pros_med, base_glute_med, base_psoas_med)
        pat_df = pat_df[pat_df["DaysDiff"] != 0]
        #print(pat_df.head())
        scans = pat_df["Scan"].unique()
        
        for s in scans:
            #print(i)
            PatID = UF.FixPatID(i)
            #print(d)
            day_df = pat_df[pat_df["Scan"] == s]
            print("Patient: {} Scan: {}".format(PatID, s))
          
            #med_value = day_df["Median"].iloc[0]
            #
            image_path = url + t + "\\" +PatID+ "\\" + s + "\\BaseImages\\" +PatID+ "_" + s + "_Raw.nii"
            #masks_path = url + t + "\\" +PatID+ "\\" + s + "\\Masks\\"
            for r in Regions:
                region_df = day_df[pat_df["Region"] == r]
                mean_value = region_df["Mean"].iloc[0]
                med_value = region_df["Median"].iloc[0]
                
                if r == "Prostate":
                    mean_factor = base_pros_mean / mean_value
                    med_factor = base_pros_med / med_value
                    #base_value = base_pros_
                    mask_label = "_shrunk_pros.nii"
                    med_label = "Med-Pros"
                elif r == "Glute":
                    mean_factor = base_glute_mean / mean_value
                    med_factor = base_glute_med / med_value
                    #base_value = base_glute
                    mask_label = "_glute.nii"
                    med_label = "Med-Glute"
                elif r == "Psoas":
                    mean_factor = base_psoas_mean / mean_value
                    med_factor = base_psoas_med / med_value
                    #base_value = base_psoas
                    mask_label = "_psoas.nii"
                    med_label = "Med-Psoas"
                

                #print(r, mean_value, mean_factor,  med_value, med_factor)
                #mask_path = masks_path +PatID+ "_" + s + mask_label
                med_path = url + t + "\\" +PatID+ "\\" + s + "\\" + med_label + "\\" +PatID+ "_" + s + "_" + med_label + ".nii"

                UF.NormImage(image_path, med_factor, med_path)