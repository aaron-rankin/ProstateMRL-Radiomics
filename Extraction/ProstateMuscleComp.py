"""""

Aaron Rankin 08/03/22
Reads in nifti images, prostate contours and glute clicks (outside dose field) and calculates mean and std
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
url_20f_new = 'D:/data/prostateMR_radiomics/nifti/20fractions_new/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
url_SABR_new = 'D:/data/prostateMR_radiomics/nifti/SABR_new/'

# set working directories
url = url_20f
scan_info_url = 'D:\data\Aaron\ProstateMRL\Data\Extraction\patientDatainfo\scaninfo_20fractions.csv'

# change depending on dataset
output = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\DataFiles\\20fractions.csv"

ptDir = os.listdir(url)
print("Patient Directory: " + url)
print(ptDir)
print("Output Directory: " + output)

df_all = pd.DataFrame(columns=("PatID", "ScanDate", "Scan", "ScanTime", "Observer", "Region", "Mean", "Std"))
col_list = ["Patient", "Scan", "DateofScan"]
scan_info = pd.read_csv(scan_info_url, skipinitialspace=True, index_col=False)

print(scan_info.head)
# Loop through ptDir
for i in ptDir:
    scanWeeks = os.listdir(url+str(i))
    print(scanWeeks) 
    patient = [i.lstrip('0')]
   # print(patient)
    
    scanValues = {"PatID":[], "ScanDate":[], "Scan":[], "ScanTime":[], "Observer": [], "Region": [], "Mean":[], "Std":[]}
    scanValues["PatID"] = str(i)

    temp_df1 = scan_info[scan_info["Patient"].isin(patient)]

    # Loop through patient visits
    for j in scanWeeks:
        niiFiles = os.listdir(url+str(i)+"\\"+str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        imageName = i +" "+ j

        image = url+str(i)+"\\"+str(j)+"\\"+str(i)+"_"+str(j)+"_image.nii"
        bodyMask = url+str(i)+"\\"+str(j)+"\\"+str(i)+"_"+str(j)+"_body_mask.nii"

        readImage = sitk.ReadImage(image)
        readBodyMask = readBodyMask = sitk.ReadImage(bodyMask)

        bodyMaskArray = sitk.GetArrayFromImage(readBodyMask)
        imageArray = sitk.GetArrayFromImage(readImage)

        # remove stray pixel values 
        imageArray = imageArray * bodyMaskArray

        scanNum = str(j)
        scanNum = int(scanNum[2:])
        scanValues["Scan"] = scanNum
        scan = [j]

        temp_df = temp_df1[temp_df1["Scan"].isin(scan)]
        temp_df["DateofScan"] = temp_df["DateofScan"].apply(str)

        Date = str(temp_df["DateofScan"])
        Date = str(Date).split("    ")
        Date = str(Date[1]).split("\n")
        Date = str(Date[0])
        year, month, day = Date[0:4], Date[4:6], Date[6:8]
        #print(day+"-"+month+"-"+year)
        newDate = str(day + "-" + month + "-" + year)
        scanValues["ScanDate"] = (newDate)

        Time = temp_df["TimeofScan"]
        scanValues["ScanTime"] = Time

        for k in niiFiles:

            if "glute" in k:
                gluteMask = url + str(i) + "\\" + str(j) + "\\" + str(k)
                readgluteMask = sitk.ReadImage(gluteMask)
                gluteMaskArray = sitk.GetArrayFromImage(readgluteMask)

                maskName = str(k)
                maskName = maskName[:-4]
                print("Mask: " + maskName)

                Observer = "AR"
                scanValues["Observer"] = Observer

                scanValues["Region"] = "Glute"

                #readImage = sitk.ReadImage(image)
                #imageArray = sitk.GetArrayFromImage(readImage)
                # remove stray pixel values
                #imageArray = imageArray * bodyMaskArray

                maskedImageglute = ma.masked_array(imageArray, mask=(gluteMaskArray), keep_mask=True, hard_mask=True)
                meanglute = np.abs(np.mean(maskedImageglute.flatten()))
                stdglute = np.abs(np.std(maskedImageglute.flatten()))

                scanValues["Mean"] = meanglute
                scanValues["Std"] = stdglute

                df_all = df_all.append(scanValues, ignore_index=True)
                df_all["Scan"] = pd.to_numeric(df_all["Scan"])
                df_all["ScanDate"] = pd.to_datetime(df_all["ScanDate"], dayfirst=True)

            elif "psoas" in k:
                psoasMask = url + str(i) + "\\" + str(j) + "\\" + str(k)
                readpsoasMask = sitk.ReadImage(psoasMask)
                psoasMaskArray = sitk.GetArrayFromImage(readpsoasMask)

                maskName = str(k)
                maskName = maskName[:-4]
                print("Mask: " + maskName)

                Observer = "AR"
                scanValues["Observer"] = Observer

                scanValues["Region"] = "psoas"

                #readImage = sitk.ReadImage(image)
                #imageArray = sitk.GetArrayFromImage(readImage)
                # remove stray pixel values
                #imageArray = imageArray * bodyMaskArray

                maskedImagepsoas = ma.masked_array(imageArray, mask=(psoasMaskArray), keep_mask=True, hard_mask=True)
                meanpsoas = np.abs(np.mean(maskedImagepsoas.flatten()))
                stdpsoas = np.abs(np.std(maskedImagepsoas.flatten()))

                scanValues["Mean"] = meanpsoas
                scanValues["Std"] = stdpsoas

                df_all = df_all.append(scanValues, ignore_index=True)
                df_all["Scan"] = pd.to_numeric(df_all["Scan"])
                df_all["ScanDate"] = pd.to_datetime(df_all["ScanDate"], dayfirst=True)

            elif "ostate" in k:                       
                scanValues["Region"] = "Prostate"
                maskName = str(k)
                maskName = maskName[:-4]
                
                segmentation = True
                mask = url+str(i)+"\\"+str(j)+"\\"+str(k)
                print("Mask: " + maskName)

                Observer = maskName.replace(i, "")
                Observer = Observer.replace(j, "")
                Observer = Observer.replace("Prostate", "")
                Observer = Observer.replace("_", "")

                scanValues["Observer"] = Observer
               
                # read in prostate mask
                readprosMask = sitk.ReadImage(mask)
                maskArray = sitk.GetArrayFromImage(readprosMask)

                # use prostate mask on whole image
                maskedImagePros = ma.masked_array(imageArray, mask=np.logical_not(maskArray), keep_mask=True, hard_mask=True)
                meanPros = np.mean(maskedImagePros.flatten())
                stdPros = np.std(maskedImagePros.flatten())
                
                scanValues["Mean"] = meanPros
                scanValues["Std"] = stdPros
                
                df_all = df_all.append(scanValues, ignore_index=True)
                df_all["Scan"] = pd.to_numeric(df_all["Scan"])
                df_all["ScanDate"] = pd.to_datetime(df_all["ScanDate"], dayfirst=True)

  
df_all.to_csv(output)

print(df_all.head)
print("---------- Done ----------")