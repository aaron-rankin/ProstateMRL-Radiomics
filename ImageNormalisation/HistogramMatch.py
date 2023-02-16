import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
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

HM_type = "HM-FSTP"

# filter only SABR patients
patKey = patKey[patKey["Treatment"] == "SABR"]
PatIDs = patKey["PatID"].unique()

if HM_type == "HM-FSTP":
    refTP = "D:\data\prostateMR_radiomics\\nifti\SABR_new\\1431\\MR1\\RawImages\\1431_MR1_Raw.nii"
    TPimg = sitk.ReadImage(refTP)

for pat in tqdm(PatIDs):
    p_df = patKey[patKey["PatID"].isin([pat])]
    patDir = p_df["FileDir"].values[0]
   
    pat = UF.FixPatID(pat, patDir)
    patDir = niftiDir + patDir + "\\" + pat + "\\" 
    
    scans = p_df["Scan"].values
    FS = scans[0]
    print("Pat - {}, Scans - {}, FS - {}".format(pat, scans, FS))

    imgFS = patDir + "{}\\RawImages\\{}_{}_Raw.nii".format(FS, pat, FS)
    refimg = sitk.ReadImage(imgFS)

    for scan in scans:
        scanDir = patDir + "\\" + scan + "\\"

        rawimg = scanDir + "RawImages\\{}_{}_Raw.nii".format(pat, scan)
        rawimg = sitk.ReadImage(rawimg)
        matcher = sitk.HistogramMatchingImageFilter()
        matcher.SetNumberOfHistogramLevels(512)
        matcher.SetNumberOfMatchPoints(32)
        matcher.ThresholdAtMeanIntensityOn()

        HMimg = matcher.Execute(rawimg, refimg)

        if HM_type == "HM-FSTP":
            HMimg = matcher.Execute(HMimg, TPimg)

        sitk.WriteImage(HMimg, scanDir + "{}\\{}_{}_{}.nii".format(HM_type, pat, scan, HM_type))

        