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
csv_url = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\ScanInfo\\"
packedIDs = os.listdir(csv_url)

# strip .csv
for p in range(len(packedIDs)):
    q = packedIDs[p]
    packedIDs[p] = q[:-4]

url_SABR = "D:\\data\\prostateMR_radiomics\\nifti\\SABR\\"
url_20f = "D:\\data\\prostateMR_radiomics\\nifti\\20fractions\\"

url = url_20f

ptDir = os.listdir(url)

print(packedIDs)
print(ptDir)

#packedIDs = ['0001088', '0001089', '0001118', '0001303', '0001307']

for i in ptDir:
    patID_s = i
    if patID_s in packedIDs:
               
        # read in pat csv
        pat_df = pd.read_csv((csv_url + patID_s + ".csv"))
        fractions = pat_df.Fraction.unique()
        visits = pat_df.MRContour.unique()
        
        # get base values (Frac 1, Scan 1 - for now)
        base_df = pat_df.loc[pat_df["Fraction"]==fractions[0]]
        print(base_df.head())
        base_path = url + str(i) + "\\" + visits[0][1:] + "\\"
        base_image = base_path + "\\BaseImages\\" + str(i)+ "_" + visits[0][1:] + "_image.nii"
       # base_pros = UF.MaskedMeanStd(base_image, base_path + "Masks\\" + str(i) + "_" + visits[0][1:] + "_shrunk_pros.nii")[0]
       # base_glute = UF.MaskedMeanStd(base_image, base_path + "Masks\\" + str(i) + "_" + visits[0][1:] + "_glute.nii")[0]
        base_psoas = UF.MaskedMeanStd(base_image, base_path + "Masks\\" + str(i) + "_" + visits[0][1:] + "_psoas.nii")[0]
        

        for j in fractions:
            MRcont = pat_df[pat_df["Fraction"] == j]["MRContour"].iloc[0]
            MRcont = MRcont[1:]
            pat_path = url + str(i) + "\\" + MRcont + "\\"

            contour_df = pat_df.loc[pat_df["MRContour"] == (MRcont)] 
            
            base_vals = [base_psoas]#[base_pros, base_glute, 
            # get reg images
            rawimg_folder = pat_path + "BaseImages\\"
            rawimgs = os.listdir(rawimg_folder)
            
            print("Patient: " + str(i) + " Timepoint: " + MRcont)
            print("------------------------------")

            rawimg_path = rawimg_folder + str(i) + "_" + MRcont + "_image.nii"
            pros_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + MRcont + "_shrunk_pros.nii")
            glute_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + MRcont + "_glute.nii")
            psoas_path = os.path.join(pat_path, "Masks\\", str(i) + "_" + MRcont + "_psoas.nii")
            masks = [psoas_path]#[pros_path, glute_path, 

            factors_labels =["Norm-Psoas"]# ["Norm-Pros", "Norm-Glute",

            for l in range(1):
                mean = UF.MaskedMeanStd(rawimg_path, masks[l])[0]
                factor = base_vals[l] / mean
                image = sitk.ReadImage(rawimg_path)
                image_array= sitk.GetArrayFromImage(image)
                norm_image_array = image_array * factor
                
                new_path = pat_path + factors_labels[l] + "\\" + str(i) + "_" + MRcont + "_" + factors_labels[l] + "_test.nii"

                norm_image = sitk.GetImageFromArray(norm_image_array)
                norm_image.SetDirection(image.GetDirection())
                norm_image.SetSpacing(image.GetSpacing())
                norm_image.SetOrigin(image.GetOrigin())
                sitk.WriteImage(norm_image, new_path)
    
