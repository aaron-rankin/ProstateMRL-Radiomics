"""""

Aaron Rankin 08/03/22
Reads in nifti images, prostate contours and muscle clicks (outside dose field) and calculates mean and std
Saves to csv

"""""
from cProfile import label
import string
from turtle import title
from wsgiref.simple_server import sys_version
import SimpleITK as sitk
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd



# check version of libraries (Py 3.6.5, PyRad 3.0)
print("Python version: " + sys_version)

# patient nifti directories
url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_20f_new = 'D:/data/prostateMR_radiomics/nifti_new/new_20fractions/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
url_SABR_new = 'D:/data/prostateMR_radiomics/nifti_new/new_SABR/'

# output directories
out_20f = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions\\"
out_20f_new = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions_new\\"
out_SABR = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR\\"
out_SABR_new = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR_new\\"

# set working directories
url = url_SABR

# change depending on dataset
output = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions.csv"


ptDir = os.listdir(url)
print("Patient Directory: " + url)
print(ptDir)
print("Output Directory: " + output)

if "new" in url:            # for new patients  (one contour)
    check = "RP"
else:                       # for original patients (multiple contours)
    check = "ostate"

df_all = pd.DataFrame(columns=("PatID", "Scan", "Observer", "Mean Prostate", "Std Prostate", "Mean Muscle", "Std Muscle"))

# Loop through ptDir
for i in ptDir:
    scanWeeks = os.listdir(url+str(i))
    print(scanWeeks) 
    
    scanValues = {"PatID":[], "Scan":[], "Observer": [], "Mean Prostate":[], "Std Prostate":[], "Mean Muscle":[], "Std Muscle":[]}
    scanValues["PatID"] = str(i)

    # Loop through patient visits
    for j in scanWeeks:
        niiFiles = os.listdir(url+str(i)+"\\"+str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        imageName = i +" "+ j
        image = url+str(i)+"\\"+str(j)+"\\"+str(i)+"_"+str(j)+"_image.nii"

        scanNum = str(j)
        scanNum = int(scanNum[2:])
        scanValues["Scan"] = scanNum
    
        
        # Loop through patient files
        for k in niiFiles:
            # load in body masks
            if "body_mask" in k:
                bodyMask = url + str(i) + "\\" + str(j) + "\\" + str(k)
                readBodyMask = sitk.ReadImage(bodyMask)
                bodyMaskArray = sitk.GetArrayFromImage(readBodyMask)
            
            if check in k:                       
                maskName = str(k)
                maskName = maskName[:-4]
                
                segmentation = True
                mask = url+str(i)+"\\"+str(j)+"\\"+str(k)
                print("Mask: " + maskName)
                
                if "new" in url: 
                    Observer = maskName.replace(j, "")
                    Observer = Observer.replace(i, "")
                    Observer = Observer.replace("_", "")
                else:
                    Observer = maskName.replace(j, "")
                    Observer = Observer.replace("Prostate", "")
                    Observer = Observer.replace("_", "")

                print(Observer)
                scanValues["Observer"] = Observer
                
                # read in whole image
                readImage = sitk.ReadImage(image)
                imageArray = sitk.GetArrayFromImage(readImage)
                # remove stray pixel values
                imageArray = imageArray * bodyMaskArray
                #print(imageArray.shape)
                #print(np.mean(imageArray.flatten()))
               
                # read in mask
                readMask = sitk.ReadImage(mask)
                maskArray = sitk.GetArrayFromImage(readMask)

                maskedImagePros = ma.masked_array(imageArray, mask=np.logical_not(maskArray), keep_mask=True, hard_mask=True)
                meanPros = np.mean(maskedImagePros.flatten())
                stdPros = np.std(maskedImagePros.flatten())
                
                scanValues["Mean Prostate"] = meanPros
                scanValues["Std Prostate"] = stdPros

                maskedImageMuscle = ma.masked_array(imageArray, mask=np.logical_not(muscleArray), keep_mask=True, hard_mask=True)
                meanMuscle = np.mean(maskedImageMuscle.flatten())
                stdMuscle = np.std(maskedImageMuscle.flatten())

                df_all = df_all.append(scanValues, ignore_index=True)
                df_all["Scan"] = pd.to_numeric(df_all["Scan"])

  
df_all.to_csv(output)

print(df_all.head)
print("---------- Done ----------")