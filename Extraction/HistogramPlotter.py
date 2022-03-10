"""""
Aaron Rankin 08/03/22
Reads in nifti files of whole MR, body mask and contour
Plots histogram of whole image and within contours

Change to just lines - no fill, more bins

"""""
from cProfile import label
from wsgiref.simple_server import sys_version
import SimpleITK as sitk
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys

# check version of libraries (Py 3.6.5, PyRad 3.0)
print("Python version: " + sys_version)

# patient nifti directories
url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_20f_new = 'D:/data/prostateMR_radiomics/nifti_new/new_20fractions/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
url_SABR_new = 'D:/data/prostateMR_radiomics/nifti_new/new_SABR/'

# output directories
out_20f = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Histograms\\Raw\\20fractions\\"
out_20f_new = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Histograms\\Raw\\20fractions_new\\"
out_SABR = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Histograms\\Raw\\SABR\\"
out_SABR_new = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Histograms\\Raw\\SABR_new\\"

# set working directories
url = url_SABR_new
output = out_SABR_new

ptDir = os.listdir(url)
print("Patient Directory: " + url)
print(ptDir)
print("Output Directory: " + output)

if "new" in url:            # for new patients  (one contour)
    check = "RP"
else:                       # for original patients (multiple contours)
    check = "ostate"


# Loop through ptDir
for i in ptDir: 
    scanWeeks = os.listdir(url+str(i))
    
    # Loop through patient visits
    for j in scanWeeks:
        niiFiles = os.listdir(url+str(i)+"\\"+str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        imageName = i +" "+ j
        image = url+str(i)+"\\"+str(j)+"\\"+str(i)+"_"+str(j)+"_image.nii"

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
                
                # read in whole image
                readImage = sitk.ReadImage(image)
                imageArray = sitk.GetArrayFromImage(readImage)
                # remove stray pixel values
                imageArray = imageArray * bodyMaskArray

                # read in mask
                readMask = sitk.ReadImage(mask)
                maskArray = sitk.GetArrayFromImage(readMask)

                # for plotting intensity only in contour
                #maskedImage = maskArray * imageArray
                maskedImage = ma.masked_array(imageArray, mask=np.logical_not(maskArray), keep_mask=True, hard_mask=True)

                maskedImage = maskedImage.flatten()
                imageArray = imageArray.flatten()

                if "RP" in maskName:
                    pltColour = "tomato"
                elif "JZ" in maskName:
                    pltColour = "limegreen"
                elif "MA" in maskName:
                    pltColour = "dodgerblue"
                else:
                    pltColour = "purple"

                print("max: " + str(imageArray.max()))
                # Open figure
                plt.figure("Intensity Histogram")
                plt.title("Patient: " + i + " " + j)
                
                plt.hist(maskedImage, bins = 256, range=(1, imageArray.max()), alpha = 0.5, histtype = "step", color=pltColour, fill = True, density = True, label = maskName)
                plt.xlabel("MR Intensity")
                plt.xlim(0,400)
                plt.ylim(0, 0.03)
                plt.ylabel("Percentage")
                
            else:
                segmentation = False

        outputfolder = output #+ i
        if not os.path.exists(outputfolder):
            os.mkdir(outputfolder)
        else:
            print()
        plt.hist(imageArray, bins = 256, range=(1, imageArray.max()), facecolor = "blue", alpha = 0.75, color = "black", fill = False, histtype = "step", density = True, label = "WholeImage")
        plt.legend()
        plt.savefig(outputfolder + str(i) + "_" + str(j)+ "_newtest.png", dpi = 300)
        plt.clf()
            
               
        if segmentation == False:
            print ("Check segmentation list for "+j)

print("---------- Done ----------")