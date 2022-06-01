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

csv_url = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\MeanValues\\"
packedIDs = os.listdir(csv_url)

# strip .csv
for p in range(len(packedIDs)):
    q = packedIDs[p]
    packedIDs[p] = q[:-4]

url_SABR = "D:\\data\\prostateMR_radiomics\\nifti\\SABR\\"
url_20f = "D:\\data\\prostateMR_radiomics\\nifti\\20fractions\\"

url = url_SABR

ptDir = os.listdir(url)
for i in ptDir:
    patID_s = str.lstrip(i, "0000")
    if patID_s in packedIDs:
        visits = os.listdir(url + str(i) + "\\")

        # read in pat csv
        pat_df = pd.read_csv((csv_url + patID_s + ".csv"))
        # get base values (Frac 1, Scan 1 - for now)
        base_df = pat_df[pat_df["Fraction"].isin([1])]
        base_df = base_df[base_df["Scan"].isin([1])]

        base_pros, base_glute, base_psoas = base_df.iloc[0]["ShrunkProstate"], base_df.iloc[0]["Glute"], base_df.iloc[0]["Psoas"]

        for j in visits:
            print("Patient: " + str(i) + " Timepoint: " + str(j))
            pat_path = url + str(i) + "\\" + str(j) + "\\"

            contour_df = pat_df.loc[pat_df["MRContour"] == (" " + j)] # there's a space in the cell

            # get reg images
            rawimg_folder = pat_path + "Reg-Raw\\"
            rawimgs = os.listdir(rawimg_folder)

            for k in rawimgs:
                scan_num = int(k[-5:-4])
                print("Scan Number: " + str(scan_num))

                scan_df = contour_df[contour_df["Scan"] == (scan_num)]
                scan_pros, scan_glute, scan_psoas = scan_df.iloc[0]["ShrunkProstate"], scan_df.iloc[0]["Glute"], scan_df.iloc[0]["Psoas"]

                rawimg_path = rawimg_folder + str(i) + "_" + str(j) + "_reg_img_" + str(scan_num) + ".nii"

                factor_pros, factor_glute, factor_psoas = (base_pros/scan_pros), (base_glute/scan_glute), (base_psoas/scan_psoas)
                factors_values = [factor_pros, factor_glute, factor_psoas]
                factors_labels = ["Norm-Pros", "Norm-Glute", "Norm-Psoas"]

                image = sitk.ReadImage(rawimg_folder + k)
                image_array = sitk.GetArrayFromImage(image)

                for l in range(3):
                    norm_image_array = image_array * factors_values[l]
                    
                    new_path = pat_path + "Norm-Images" + "\\" + str(i) + "_" + str(j) + "_" + factors_labels[l] + "_" + str(scan_num) + ".nii"

                    norm_image = sitk.GetImageFromArray(norm_image_array)
                    sitk.WriteImage(norm_image, new_path)
