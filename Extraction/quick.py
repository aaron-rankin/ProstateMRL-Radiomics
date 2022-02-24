import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys
from scipy.ndimage import binary_dilation, binary_erosion, generate_binary_structure

url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_20f_new = 'D:/data/prostateMR_radiomics/nifti_new/new_20fractions/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
url_SABR_new = 'D:/data/prostateMR_radiomics/nifti_new/new_SABR/'

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

        # Loop through patient files
        for k in niiFiles:   
            if "BodyMask" in k:
                print(url+i+"\\"+j+"\\"+k)
                os.remove(url+i+"/"+j+"/"+k)
                
