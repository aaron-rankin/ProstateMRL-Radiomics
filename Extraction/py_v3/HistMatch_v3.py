import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import UsefulFunctions as UF
import pandas as pd

HM = "HM-TP"

key_df = pd.read_csv("D:\data\Aaron\ProstateMRL\Data\MRLPacks\\All_PatientKey.csv")

url = "D:\\data\\prostateMR_radiomics\\nifti\\"

t_dir = key_df.FileDir.unique()
print(t_dir)
##########################################
# 0: 20f, 1: 20f_new, 2: SABR, 3: SABR_new
##########################################
#t_dir = t_dir[2:3]
for t in t_dir:
    print(t)
    t_df = key_df.loc[key_df["FileDir"] == t]
    patIDs = t_df.PatID.unique()
    print(patIDs)


    for i in patIDs:
        pat_df = t_df[t_df["PatID"].isin([i])]
        
        if "new" in t:
            patID = str(i)
        else:
            i = UF.FixPatID(i,t)
            patID = i 
        scans = pat_df.Scan.unique()
       
        print("-"*50)
        
        for j in scans:
            MRscan = j
            image_path = url + str(t) + "\\" + patID + "\\" + MRscan + "\\RawImages\\" + patID + "_" + MRscan + "_Raw.nii"

            first_scan = scans[0]
            refPatTP = 'D:/data/prostateMR_radiomics/nifti/SABR/0001307/MR6/RawImages/0001307_MR6_Raw.nii' # if HM2 - ref scan is first scan per patient
            refPatFS = url + str(t) + "\\" + patID + "\\" + first_scan + "\\RawImages\\" + patID + "_" + first_scan + "_Raw.nii"

            if HM == "HM-TP":
                refPat = refPatTP
            elif HM == "HM-FS" or "HM-FSTP":
                refPat = refPatFS
            refimage =  sitk.ReadImage(refPat) 
            result = sitk.GetArrayFromImage(refimage)
            result = result.flatten()
            refmax = result.max()
            
            
            print('Processing patient: ' + patID + '   scan: ' + MRscan)

            image = sitk.ReadImage(url + t + "\\" + patID + '/' + MRscan + '/RawImages/' + str(i) + "_" + MRscan + "_Raw.nii")
            
            matcher = sitk.HistogramMatchingImageFilter()
            matcher.SetNumberOfHistogramLevels(512)
            matcher.SetNumberOfMatchPoints(32)
            matcher.ThresholdAtMeanIntensityOn()

            if HM == "HM-FSTP":
                image = matcher.Execute(image, refimage)
                refimageTP = sitk.ReadImage(refPatTP)
                image = matcher.Execute(image, refimageTP)
            else:
                image = matcher.Execute(image, refimage)

            
            sitk.WriteImage(image, url + str(t) + "\\" + patID + "\\" + MRscan + "\\" + HM + "\\" + patID + "_" + MRscan + "_" + HM + ".nii")
