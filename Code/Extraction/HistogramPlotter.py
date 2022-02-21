from wsgiref.simple_server import sys_version
import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import radiomics
import sys

# check version of libraries (Py 3.6.5, PyRad 3.0)
print("Python version: " + sys_version)
print ("PyRadiomics version: " + radiomics.__version__)

url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
ptDir = os.listdir(url_20f)


# Loop through ptDir
for i in ptDir:
    scanWeeks = os.listdir(url_20f+str(i))
    
    # Loop through patient visits
    for j in scanWeeks:
        niiFiles = os.listdir(url_20f+str(i)+"\\"+str(j))
        # print(niiFiles)
        print ("Processing: "+i+"  Timepoint: "+j)	
        imageName = i +" "+ j
        image = url_20f+str(i)+"\\"+str(j)+"\\"+str(i)+"_"+str(j)+"_image.nii"
        print ("Image: "+ imageName)

        # Loop through patient files
        for k in niiFiles:
            x = "ostate"
            if x in k:
                maskName = str(k)
                segmentation = True
                mask = url_20f+str(i)+"\\"+str(j)+"\\"+str(k)
                print("Mask: " + maskName)
                
                # read in whole image
                readImage = sitk.ReadImage(image)
                imageArray = sitk.GetArrayFromImage(readImage)
                #imageArray = imageArray.flatten()

                # read in mask
                readMask = sitk.ReadImage(mask)
                maskArray = sitk.GetArrayFromImage(readMask)
                #maskArray = maskArray.flatten()

                maskedImage = maskArray * imageArray

                maskedImage = maskedImage.flatten()
                imageArray = imageArray.flatten()
                
                # Open figure
                plt.figure("Intensity Histogram")
                plt.hist(imageArray, bins = 128, range=(1, imageArray.max()), facecolor = "red", alpha = 0.75, histtype = "step", density = True)
                plt.hist(maskedImage, bins = 64, range=(1, imageArray.max()), facecolor = "blue", alpha = 0.75, histtype = "step", fill = True, density = True)
                plt.xlabel("MR Intensity")
                plt.ylabel("Percentage")

                outputfolder = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Histograms\\Raw\\20fractions\\" + str(i)
                if not os.path.exists(outputfolder):
                    os.mkdir(outputfolder)
                else:
                    print()

                plt.savefig("D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Histograms\\Raw\\20fractions\\" + str(i) + "\\" + str(i) + "_" + str(j) + "_" + str(k) ".png", dpi = 300)
                plt.clf()
            else:
                segmentation = False
               
        if segmentation == False:
            print ("Check segmentation list for "+j)
