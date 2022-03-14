"""""

Aaron Rankin 08/03/22
Reads in nifti images, prostate contours and muscle clicks (outside dose field) and calculates mean and std
Saves to csv

"""""
from cProfile import label
from operator import index
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

# set working directories
url = url_20f
scan_info_url = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\patientDatainfo\\scaninfo_20fractions.csv"

# change depending on dataset
output = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\DataFiles\\20fractions.csv"


ptDir = os.listdir(url)
print("Patient Directory: " + url)
print(ptDir)
print("Output Directory: " + output)

df_all = pd.DataFrame(columns=("PatID", "ScanDate", "Scan", "Observer", "Region", "Mean", "Std"))
col_list = ["Patient", "Scan", "DateofScan"]
scan_info = pd.read_csv(scan_info_url, skipinitialspace=True, index_col=False)

print(scan_info.head)
# Loop through ptDir
for i in ptDir:
    scanWeeks = os.listdir(url+str(i))
    print(scanWeeks) 
    patient = [i.lstrip('0')]
   # print(patient)
    
    scanValues = {"PatID":[], "ScanDate":[], "Scan":[], "Observer": [], "Region": [], "Mean":[], "Std":[]}
    scanValues["PatID"] = str(i)

    temp_df1 = scan_info[scan_info["Patient"].isin(patient)]
    #print(patient)
    #print(temp_df1)

    # Loop through patient visits
    for j in scanWeeks:
        niiFiles = os.listdir(url+str(i)+"\\"+str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        imageName = i +" "+ j
        image = url+str(i)+"\\"+str(j)+"\\"+str(i)+"_"+str(j)+"_image.nii"

        scanNum = str(j)
        scanNum = int(scanNum[2:])
        scanValues["Scan"] = scanNum
        scan = [j]

        temp_df = temp_df1[temp_df1["Scan"].isin(scan)]
        temp_df["DateofScan"] = temp_df["DateofScan"].apply(str)
        #DoS = temp_df['DateofScan']        
        #print(DoS)
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
            
            if "ostate" in k:                       
                scanValues["Region"] = "Prostate"
                maskName = str(k)
                maskName = maskName[:-4]
                
                segmentation = True
                mask = url+str(i)+"\\"+str(j)+"\\"+str(k)
                print("Mask: " + maskName)

                Observer = maskName.replace(i, "")
                Observer = maskName.replace(j, "")
                Observer = Observer.replace("Prostate", "")
                Observer = Observer.replace("_", "")

                print(Observer)
                scanValues["Observer"] = Observer

                Date = str(temp_df["DateofScan"])
                print(Date)
                Date = str(Date).split("    ")
                Date = str(Date[1]).split("\n")
                print(Date[1])
                Date = str(Date[0])
                day, month, year = str(Date[6:]), str(Date[4:6]), str(Date[0:4])
                year, month, day = Date[0:4], Date[4:6], Date[6:8]
                #print(day+"-"+month+"-"+year)
                print("Day: "+day)
                print("month: "+ month)
                print("year: " + year)
                newDate = str(day + "_" + month + "_" + year)
                print(newDate)
                scanValues["ScanDate"] = (newDate)
                

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
                elif "muscle" in k:
                    maskedImageMuscle = ma.masked_array(imageArray, mask=np.logical_not(muscleArray), keep_mask=True, hard_mask=True)
                    meanMuscle = np.mean(maskedImageMuscle.flatten())
                    stdMuscle = np.std(maskedImageMuscle.flatten())
                """
                
                df_all = df_all.append(scanValues, ignore_index=True)
                df_all["Scan"] = pd.to_numeric(df_all["Scan"])

  
df_all.to_csv(output)

print(df_all.head)
print("---------- Done ----------")