'''
Loop through patient directory with patients who have reg/normalised images
Load in first image at each fraction - need to load in scaninfo csv and find image
6 images - raw, Norm-Pros/Glute/Psoas, HM-TP/FS
3 masks - Prostate, Glute, Psoas
Calc mean signal and std

Output to csv:
PatID | Fraction | Contour | Date | Normalisation | Region | Mean Signal | Std Signal | d-Days | d-Mean Signal |

'''
from pydoc import pathdirs
import SimpleITK as sitk
from matplotlib.pyplot import contour
import numpy as np
import pandas as pd
import os
import UsefulFunctions as UF
from datetime import datetime

# csv_url = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges\\"
scans_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\PatientKey_sorted.csv")
treatments = ["SABR"] #"20fractions",

url = "D:\\data\\prostateMR_radiomics\\nifti\\"

output_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges_v2\\"
col_names = ["PatID","Treatment","Date","MRScan","Normalisation","Region","DaysDiff","MeanSignal","MeanDiff"]
all_df = pd.DataFrame()


for t in treatments:
    t_df = scans_df.loc[scans_df["Treatment"] == t]
    patIDs = t_df.Patient.unique()
    print(patIDs)

    for i in patIDs:
        # read in pat csv
        pat_df = t_df[t_df["Patient"].isin([i])]
        i = UF.FixPatID(i)
        patID = i 
        scans = pat_df.Scan.unique()
        vals_df = pd.DataFrame(columns=col_names)
        
        for j in scans:
            MRcont = j
            pat_path = url + str(t) + "\\" + str(i) + "\\" + MRcont + "\\"

            scan_df = pat_df.loc[pat_df["Scan"] == (MRcont)] 

            scan_date = str(scan_df.iloc[0]["DateofScan"])
           
            if len(scan_date) != 8:
                scan_date = scan_date[:-2]
            scan_date = (datetime.strptime(str(scan_date), "%Y%m%d")).date()
           

            print("Patient: {} | Scan: {}".format(patID, MRcont))
            print("-------------------------------------------------")
            
            pat_path = os.path.join(url, t, patID, MRcont)

            mask_path = os.path.join(pat_path, "Masks\\")
            if os.path.exists(os.path.join(mask_path,patID + "_" + MRcont + "_glute2.nii")):
                masks = ["_shrunk_pros.nii", "_glute2.nii", "_psoas.nii"] # set glute2 for 20f
            else:
                masks = ["_shrunk_pros.nii", "_glute.nii", "_psoas.nii"]
            
            raw_path = os.path.join(pat_path, "BaseImages\\")
            norm_pros_path = os.path.join(pat_path, "Norm-Pros\\")
            norm_psoas_path = os.path.join(pat_path, "Norm-Psoas\\")
            norm_glute_path = os.path.join(pat_path, "Norm-Glute\\")
            # med_pros_path = os.path.join(pat_path, "Med-Pros\\")
            # med_psoas_path = os.path.join(pat_path, "Med-Psoas\\")
            # med_glute_path = os.path.join(pat_path, "Med-Glute\\")
            HM_TP_path = os.path.join(pat_path, "HM-TP\\")
            HM_FS_path = os.path.join(pat_path, "HM-FS\\")

            image_paths = [raw_path, norm_glute_path, norm_pros_path, norm_psoas_path, HM_FS_path, HM_TP_path] #med_pros_path,  med_psoas_path, med_glute_path, 
            
            for k in image_paths:
                images = os.listdir(os.path.join(pat_path,k))

                # folder empty if haven't done norm
                if len(images) != 0:

                    # only want first scan (inter-fraction changes)    

                    if k == raw_path:
                        image_name = str(i) + "_" + MRcont + "_image.nii"  
                        norm = "Raw"
                    
                    if "HM" in k:
                        image_name = images[0]
                        norm = UF.GetNorm(image_name)

                    else:
                        image_name = images[-1]
                        norm = UF.GetNorm(image_name)
                        
                    image_url = os.path.join(k,image_name)
                    print(image_name)

                    # loop through masks
                    for m in masks:
                        vals_scan = {}
                        mask_name = patID + "_" + MRcont + m
                        
                        mask_url = os.path.join(mask_path, mask_name)

                        region = UF.GetRegion(mask_name)
                        scan_mean = UF.MaskedMean(image_url, mask_url)
                        
                        # get fraction 1 values

                        if j == scans[0]:
                            frac1_date = scan_date
                            frac1_mean = scan_mean
                            diff_days, diff_mean= 0, 0

                        # calc change
                        else:
                            diff_days = UF.DateDifference(frac1_date, scan_date)
                            diff_mean = scan_mean - vals_df[(vals_df["Region"] == region) & (vals_df["Normalisation"] == norm) & (vals_df["MRScan"] == (scans[0]))]["MeanSignal"].iloc[0]                      
                            #diff_med = scan_med - vals_df[(vals_df["Region"] == region) & (vals_df["Normalisation"] == norm) & (vals_df["MRScan"] == (scans[0]))]["MedSignal"].iloc[0]

                        # append all values to dict
                        vals_scan["PatID"], vals_scan["Treatment"]  = patID, t
                        vals_scan["MRScan"], vals_scan["Date"], vals_scan["Normalisation"] = MRcont, scan_date, norm
                        vals_scan["Region"], vals_scan["MeanSignal"] = region, scan_mean
                        vals_scan["DaysDiff"], vals_scan["MeanDiff"]= diff_days, diff_mean                      
                        vals_df = vals_df.append(vals_scan, ignore_index=True)
        if patID == "0001464":
            patID = patID + "_" + t 
        vals_df.to_csv(output_dir + patID + "_inter.csv")
        all_df = all_df.append(vals_df, ignore_index=True)

all_df.to_csv(output_dir + "All.csv")
print("Finished")
