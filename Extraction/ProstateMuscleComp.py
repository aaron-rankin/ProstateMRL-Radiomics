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
url_20f = 'D:/prostateMR_radiomics/nifti/20fractions/'
url_20f_new = 'D:/prostateMR_radiomics/nifti_new/new_20fractions/'
url_SABR = 'D:/prostateMR_radiomics/nifti/SABR/'
url_SABR_new = 'D:/prostateMR_radiomics/nifti_new/new_SABR/'

# set working directories
url = url_SABR_new

# change depending on dataset
output = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\DataFiles\\SABR_new.csv"


ptDir = os.listdir(url)
print("Patient Directory: " + url)
print(ptDir)
print("Output Directory: " + output)

if "new" in url:            # fsor new patients  (one contour)
    check = "RP"
else:                       # for original patients (multiple contours)
    check = "ostate"

df_all = pd.DataFrame(columns=("PatID", "Scan", "Observer", "Region", "Mean", "Std"))

# Loop through ptDir
for i in ptDir:
    scanWeeks = os.listdir(url+str(i))
    print(scanWeeks) 
    
    scanValues = {"PatID":[], "Scan":[], "Observer": [], "Region": [], "Mean":[], "Std":[]}
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
            
            """""

            Read in muscle clicks 
            
            """""
            if check in k:                       
                scanValues["Region"] = "Prostate"
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
               
                # read in prostate mask
                readprosMask = sitk.ReadImage(mask)
                maskArray = sitk.GetArrayFromImage(readprosMask)

                # use prostate mask on whole image
                maskedImagePros = ma.masked_array(imageArray, mask=np.logical_not(maskArray), keep_mask=True, hard_mask=True)
                meanPros = np.mean(maskedImagePros.flatten())
                stdPros = np.std(maskedImagePros.flatten())
                
                scanValues["Mean"] = meanPros
                scanValues["Std"] = stdPros

                """"
                maskedImageMuscle = ma.masked_array(imageArray, mask=np.logical_not(muscleArray), keep_mask=True, hard_mask=True)
                meanMuscle = np.mean(maskedImageMuscle.flatten())
                stdMuscle = np.std(maskedImageMuscle.flatten())
                """
                df_all = df_all.append(scanValues, ignore_index=True)
                df_all["Scan"] = pd.to_numeric(df_all["Scan"])

  
df_all.to_csv(output)

print(df_all.head)
print("---------- Done ----------")