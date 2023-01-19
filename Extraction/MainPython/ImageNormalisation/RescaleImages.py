import SimpleITK as sitk
from matplotlib.pyplot import contour
import numpy as np
import pandas as pd
import os
import UsefulFunctions as UF
import ImageFunctions as IF

nifti_dir = "D:\\data\\prostateMR_radiomics\\nifti\\"

csv_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\RawStats\\"
csvs = os.listdir(csv_dir)

masks = ["Pros", "Glute", "Psoas"]



for i in csvs:
    pat_df = pd.read_csv(csv_dir + i)
    
    t = pat_df.Treatment.unique()[0]

    patID = pat_df.PatID.unique()[0]

    patID = UF.FixPatID(patID,t)

    scans = pat_df.Scan.unique()
    print("####################################################")
    print("Patient: {}".format(patID))

    base_df = pat_df.loc[pat_df["DaysDiff"] == 0]
    
    base_pros_mean, base_pros_med = base_df["Mean"].iloc[0], base_df["Median"].iloc[0]
    base_glute_mean,  base_glute_med = base_df["Mean"].iloc[1], base_df["Median"].iloc[1]
    base_psoas_mean, base_psoas_med = base_df["Mean"].iloc[2], base_df["Median"].iloc[2]    
    
    base_vals = [base_pros_mean, base_pros_med, base_glute_mean, base_glute_med, base_psoas_mean, base_psoas_med]


    for MRscan in scans:
        print("Scan: {}".format(MRscan))
        pat_path = os.path.join(nifti_dir, t, patID, MRscan)
        
        scan_df = pat_df.loc[pat_df["Scan"] == (MRscan)]
        
        scan_pros_mean, scan_pros_med = scan_df["Mean"].iloc[0], scan_df["Median"].iloc[0]
        scan_glute_mean,  scan_glute_med = scan_df["Mean"].iloc[1], scan_df["Median"].iloc[1]
        scan_psoas_mean, scan_psoas_med = scan_df["Mean"].iloc[2], scan_df["Median"].iloc[2]  

        scan_vals = [scan_pros_mean, scan_pros_med, scan_glute_mean, scan_glute_med, scan_psoas_mean, scan_psoas_med]
        
        scan_path = pat_path + "\\RawImages\\" + patID + "_" + MRscan + "_Raw.nii"

        for j in range(0, 6, 2):
            mask = masks[int(j/2)]

            mean_factor = base_vals[j] / scan_vals[j]
            mean_path = pat_path + "\\Norm-" + mask + "\\" + patID + "_" + MRscan + "_Norm-" + mask + ".nii"
            IF.RescaleImage(scan_path, mean_factor, mean_path)

            med_factor = base_vals[j+1] / scan_vals[j+1]
            med_path = pat_path + "\\Med-" + mask + "\\" + patID + "_" + MRscan + "_Med-" + mask + ".nii"
            IF.RescaleImage(scan_path, med_factor, med_path)
            


                

                
                    





