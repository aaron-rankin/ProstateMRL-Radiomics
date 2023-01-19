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

print(packedIDs)
print(ptDir)


for i in ptDir:
    patID_s = i
    if patID_s in packedIDs:
        #visits = os.listdir(url + str(i) + "\\")

        # read in pat csv
        pat_df = pd.read_csv((csv_url + patID_s + ".csv"))
        # get base values (Frac 1, Scan 1 - for now)
        base_df = pat_df[pat_df["Fraction"].isin([1])]
        base_df = base_df[base_df["Scan"].isin([1])]

        base_pros, base_glute, base_psoas = base_df.iloc[0]["ShrunkProstate"], base_df.iloc[0]["Glute"], base_df.iloc[0]["Psoas"]
        base_vals = [base_pros, base_glute, base_psoas]

        visits = pat_df.MRContour.unique()

        for j in visits:
            j=j[1:]
            pat_path = url + str(i) + "\\" + str(j) + "\\"

            contour_df = pat_df.loc[pat_df["MRContour"] == (" " + j)] # there's a space in the cell

            # get reg images
            rawimg_folder = pat_path + "BaseImages\\"
            rawimgs = os.listdir(rawimg_folder)
            
            print("Patient: " + str(i) + " Timepoint: " + str(j))
            print("-----------------------")

            #for k in rawimgs:
            #scan_num = int(k[-5:-4])
            
            #print("Scan Number: " + str(scan_num))

            #scan_df = contour_df[contour_df["Scan"] == (scan_num)]

            rawimg_path = rawimg_folder + str(i) + "_" + str(j) + "_image.nii"
            pros_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + j + "_shrunk_pros.nii")
            glute_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + j + "_glute.nii")
            psoas_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + j + "_psoas.nii")
            masks = [pros_path, glute_path, psoas_path]

            #factor_pros, factor_glute, factor_psoas = (base_pros/scan_pros), (base_glute/scan_glute), (base_psoas/scan_psoas)
            #factors_values = [factor_pros, factor_glute, factor_psoas]
            factors_labels = ["Norm-Pros", "Norm-Glute", "Norm-Psoas"]

            #image = sitk.ReadImage(rawimg_path)
            #image_array = sitk.GetArrayFromImage(image)
                #print(factors_values)
            for l in range(3):
                #print("Region: " + factors_labels[l])
                mean = UF.MaskedMeanStd(rawimg_path, masks[l])[0]
                factor = base_vals[l] / mean
                image = sitk.ReadImage(rawimg_path)
                image_array= sitk.GetArrayFromImage(image)
                norm_image_array = image_array * factor
                
                new_path = pat_path + factors_labels[l] + "\\" + str(i) + "_" + str(j) + "_" + factors_labels[l] + "_test.nii"

                norm_image = sitk.GetImageFromArray(norm_image_array)
                norm_image.SetDirection(image.GetDirection())
                norm_image.SetSpacing(image.GetSpacing())
                norm_image.SetOrigin(image.GetOrigin())
                sitk.WriteImage(norm_image, new_path)
    
