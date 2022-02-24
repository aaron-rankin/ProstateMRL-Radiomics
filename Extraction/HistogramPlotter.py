from cProfile import label
from wsgiref.simple_server import sys_version
import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys

# check version of libraries (Py 3.6.5, PyRad 3.0)
print("Python version: " + sys_version)

# patient nifti directories
url_20f = 'D:/data/prostateMR_radiomics/nifti/new_20fractions/'
url_20f_new = 'D:/data/prostateMR_radiomics/nifti_new/new_20fractions/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
url_SABR_new = 'D:/data/prostateMR_radiomics/nifti_new/new_SABR/'

# set working directory
url = url_20f

ptDir = os.listdir(url)
print(ptDir)

# Loop through ptDir
for i in ptDir:
    scanWeeks = os.listdir(url+str(i))
    
    # Loop through patient visits
    for j in scanWeeks:
        niiFiles = os.listdir(url+str(i)+"\\"+str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        imageName = i +" "+ j
        image = url+str(i)+"\\"+str(j)+"\\"+str(i)+"_"+str(j)+"_image.nii"
        #print ("Image: "+ imageName)

        # Loop through patient files
        for k in niiFiles:
            # load in body masks
            if "body_mask" in k:
                bodyMask = url + str(i) + "\\" + str(j) + "\\" + str(k)
                readBodyMask = sitk.ReadImage(bodyMask)
                bodyMaskArray = sitk.GetArrayFromImage(readBodyMask)
            
            #if "ostate" in k:          # for original patients (multiple contours)
            if "RP" in k:               # for new patients  (one contour)
                maskName = str(k)
                segmentation = True
                mask = url+str(i)+"\\"+str(j)+"\\"+str(k)
                print("Mask: " + maskName)
                
                # read in whole image
                readImage = sitk.ReadImage(image)
                imageArray = sitk.GetArrayFromImage(readImage)
                # remove stray pixel values
                imageArray = imageArray * bodyMaskArray

                # read in mask
                readMask = sitk.ReadImage(mask)
                maskArray = sitk.GetArrayFromImage(readMask)

                # for plotting intensity only in contour
                maskedImage = maskArray * imageArray

                maskedImage = maskedImage.flatten()
                imageArray = imageArray.flatten()
                
                # Open figure
                plt.figure("Intensity Histogram")
                plt.title("Patient: " + i + " " + j)
                plt.hist(imageArray, bins = 128, range=(1, imageArray.max()), facecolor = "red", alpha = 0.75, histtype = "step", density = True)
                plt.hist(maskedImage, bins = 128, range=(1, imageArray.max()), facecolor = "blue", alpha = 0.75, histtype = "step", fill = True, density = True, label = "Prostate Contour")
                plt.xlabel("MR Intensity")
                plt.xlim(0,450)
                # plt.ylim(0, 0.004)
                plt.ylabel("Percentage")

                outputfolder = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Histograms\\Raw\\20fractions_new\\" + str(i)
                if not os.path.exists(outputfolder):
                    os.mkdir(outputfolder)
                else:
                    print()

                plt.savefig("D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Histograms\\Raw\\20fractions_new\\" + str(i) + "\\" + str(i) + "_" + str(j) + "_" + str(k) + ".png", dpi = 300)
                plt.clf()
            else:
                segmentation = False
               
        if segmentation == False:
            print ("Check segmentation list for "+j)
