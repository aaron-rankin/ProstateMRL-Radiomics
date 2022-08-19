'''
Read in matched images and mean values
Get mean signal of mask in frac 1 scan 1
Norm factor = frac1scan1 / fracxscanx
Multiply whole image by norm factor
'''

from pydoc import pathdirs
import SimpleITK as sitk
from matplotlib.pyplot import contour
import numpy as np
import pandas as pd
import os
import UsefulFunctions as UF

# csv_url = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges\\"
scans_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\PatientKey_sorted.csv")
treatments = ["20fractions"] #"SABR", 

url_SABR = "D:\\data\\prostateMR_radiomics\\nifti\\SABR\\"
url_20f = "D:\\data\\prostateMR_radiomics\\nifti\\20fractions\\"

url = "D:\\data\\prostateMR_radiomics\\nifti\\"


for t in treatments:
    t_df = scans_df.loc[scans_df["Treatment"] == t]
    patIDs = t_df.Patient.unique()
    print(t)
    print(patIDs)

    for i in patIDs:
        # read in pat csv
        pat_df = t_df[t_df["Patient"].isin([i])]
        i = UF.FixPatID(i) 
        scans = pat_df.Scan.unique()
        
        # get base values (Frac 1, Scan 1 - for now)
        base_df = pat_df.loc[pat_df["Scan"]==scans[0]]
        base_path = url + t + "\\" + str(i) + "\\" + scans[0] + "\\"
        base_image = base_path + "\\BaseImages\\" + str(i)+ "_" + scans[0] + "_image.nii"
        mean_pros, med_pros = UF.MaskedMeanMed(base_image, base_path + "Masks\\" + str(i) + "_" + scans[0] + "_shrunk_pros.nii")
        if os.path.exists(os.path.join(base_path + "Masks\\" + str(i) + "_" + scans[0] + "_glute2.nii")):
            mean_glute, med_glute = UF.MaskedMeanMed(base_image, base_path + "Masks\\" + str(i) + "_" + scans[0] + "_glute2.nii")
        else:
            mean_glute, med_glute = UF.MaskedMeanMed(base_image, base_path + "Masks\\" + str(i) + "_" + scans[0] + "_glute.nii")
        
        mean_psoas, med_psoas = UF.MaskedMeanMed(base_image, base_path + "Masks\\" + str(i) + "_" + scans[0] + "_psoas.nii")

        for j in scans:
            #MRcont = pat_df[pat_df["Fraction"] == j]["MRContour"].iloc[0]
            MRcont = j
            pat_path = url + str(t) + "\\" + str(i) + "\\" + MRcont + "\\"

            contour_df = pat_df.loc[pat_df["Scan"] == (MRcont)] 
            
            base_vals = [mean_pros, med_pros, mean_glute, med_glute, mean_psoas, med_psoas]
            # get reg images
            rawimg_folder = pat_path + "BaseImages\\"
            rawimgs = os.listdir(rawimg_folder)
            
            print("Patient: " + str(i) + " Timepoint: " + MRcont)
            print("------------------------------")

            rawimg_path = rawimg_folder + str(i) + "_" + MRcont + "_image.nii"
            pros_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + MRcont + "_shrunk_pros.nii")
            if os.path.exists(os.path.join(pat_path + "Masks\\" + str(i) + "_" + MRcont + "_glute2.nii")):
                glute_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + MRcont + "_glute2.nii")
            else:
                glute_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + MRcont + "_glute.nii")
            psoas_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + MRcont + "_psoas.nii")
            masks = [pros_path, glute_path, psoas_path]

            factors_labels = ["Mean-Pros", "Med-Pros", "Mean-Glute", "Med-Glute", "Mean-Psoas", "Med-Psoas"]
            
            for l in range(0,6,2):
                
                scan_val_mean, scan_val_med = UF.MaskedMeanMed(rawimg_path, masks[int(l/2)])
                factor_mean = base_vals[l] / scan_val_mean
                print(factors_labels[l] + ": {}, {}, {}".format(scan_val_mean,base_vals[l],factor_mean))
                factor_med = base_vals[l+1] / scan_val_med
                print(factors_labels[l+1] + ": {}, {}, {}".format(scan_val_med,base_vals[l+1],factor_med))
                

                file_label = str(factors_labels[l]).replace("Mean", "Norm")
                mean_path = pat_path + file_label + "\\" + str(i) + "_" + MRcont + "_" + file_label + "_v3.nii"
                med_path = pat_path + factors_labels[l+1] + "\\" + str(i) + "_" + MRcont + "_" + factors_labels[l+1] + "_v3.nii"
                
                print(mean_path, med_path)
                UF.NormImage(rawimg_path, factor_mean, mean_path)
                UF.NormImage(rawimg_path, factor_med, med_path)
            print("------------------------------")
               
                
    
