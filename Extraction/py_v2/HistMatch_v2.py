import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import UsefulFunctions as UF
import pandas as pd

HM = "HM-FS"

scans_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\PatientKey_sorted.csv")
treatments = ["SABR", "20fractions"]

url = "D:\\data\\prostateMR_radiomics\\nifti\\"


for t in treatments:
    t_df = scans_df.loc[scans_df["Treatment"] == t]
    patIDs = t_df.Patient.unique()
    print(patIDs)
    

    for i in patIDs:
        pat_df = t_df[t_df["Patient"].isin([i])]
        i = UF.FixPatID(i)
        patID = i 
        scans = pat_df.Scan.unique()
       
        
        for j in scans:
            MRcont = j
            image_path = url + str(t) + "\\" + str(i) + "\\" + MRcont + "\\BaseImages\\" + patID + "_" + MRcont + "_image.nii"

            first_scan = scans[0]
            
            if HM == "HM-TP":
                refPat = 'D:/data/prostateMR_radiomics/nifti/SABR/0001307/MR6/BaseImages/0001307_MR6_image.nii' # if HM2 - ref scan is first scan per patient
            if HM == "HM-FS":
                refPat = url + str(t) + "\\" + str(i) + "\\" + first_scan + "\\BaseImages\\" + patID + "_" + first_scan + "_image.nii"
            
            refimage =  sitk.ReadImage(refPat) 
            result = sitk.GetArrayFromImage(refimage)
            result = result.flatten()
            refmax = result.max()
            
            
            print('Processing patient: ' + i + '   scan: ' + j)

            image = sitk.ReadImage(url + t + "\\" + str(i) + '/' + MRcont + '/BaseImages/' + str(i) + "_" + MRcont + "_image.nii")
            
            matcher = sitk.HistogramMatchingImageFilter()
            matcher.SetNumberOfHistogramLevels(512)
            matcher.SetNumberOfMatchPoints(32)
            matcher.ThresholdAtMeanIntensityOn()
            image = matcher.Execute(image, refimage)
            sitk.WriteImage(image, url + str(t) + "\\" + str(i) + "\\" + MRcont + "\\" + HM + "\\" + patID + "_" + MRcont + "_" + HM + ".nii")
