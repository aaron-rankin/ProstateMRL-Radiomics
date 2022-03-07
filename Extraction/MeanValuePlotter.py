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
output = out_SABR


ptDir = os.listdir(url)
print("Patient Directory: " + url)
print(ptDir)
print("Output Directory: " + output)

if "new" in url:            # for new patients  (one contour)
    check = "RP"
else:                       # for original patients (multiple contours)
    check = "ostate"

df_all = pd.DataFrame(columns=("PatID", "Scan", "Observer", "Mean Prostate", "Mean Muscle"))

# Loop through ptDir
for i in ptDir:
    scanWeeks = os.listdir(url+str(i))
    print(scanWeeks) 

    ProsContourMeans = np.array([]) 
    MuscleContourMeans = np.array([])
    Timepoints = np.array([])

    # plt.figure("Mean Intensity Plot")
    # plt.title("Mean Signal Intensity Patient: " + i)
    # plt.ylabel("MR Intensity")
    # plt.xlabel("MR Scan")
    # #plt.xlim(0,400)
    # plt.ylim(0, 160)

    df_pat = pd.DataFrame(columns=("PatID", "Scan", "Observer", "Mean Prostate", "Mean Muscle"))
    
    scanValues = {"PatID":[], "Scan":[], "Observer": [], "Mean Prostate":[], "Mean Muscle":[]}
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
                ProsContourMeans = np.append(ProsContourMeans, meanPros)
                
                scanValues["Mean Prostate"] = meanPros
                #print(ProsContourMeans)
                #print(Timepoints)
                df_pat = df_pat.append(scanValues, ignore_index=True)
                df_pat["Scan"] = pd.to_numeric(df_pat["Scan"])


    plt.figure("Mean Intensity Plot")
    plt.title("Mean Signal Intensity Patient: " + i)
    plt.ylabel("MR Intensity")
    plt.xlabel("MR Scan")

    groupedObs = df_pat.groupby("Observer")
    for name, group in groupedObs:
        fig = plt.plot(groupedObs["Scan"], groupedObs["Mean Prostate"], marker="o", linestyle="", label = name)
    plt.legend
    fig.savefig(output + str(i) + ".png", dpi = 300)
    plt.clf

    df_all = df_all.append(df_pat)
    # plt.scatter(x=Timepoints, y=ProsContourMeans)
    # print(ProsContourMeans)            
    # # outputfolder = output + i
    # # if not os.path.exists(outputfolder):
    # #     os.mkdir(outputfolder)
    # # else:
    # #     print()
    # # plt.hist(imageArray, bins = 256, range=(1, imageArray.max()), facecolor = "blue", alpha = 0.75, color = "black", fill = False, histtype = "step", density = True, label = "WholeImage")
    # # plt.legend()
    # plt.savefig(output + str(i) + ".png", dpi = 300)
    # plt.clf()
        
  
# df.to_csv(output+"data.csv")

print(df_all)
print("---------- Done ----------")