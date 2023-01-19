"""""
Aaron Rankin 08/03/22
Reads in nifti files of whole MR, body mask and contour
Plots histogram of whole image and within contours

Change to just lines - no fill, more bins

"""""

from email.quoprimime import body_check
import SimpleITK as sitk
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys


def ReadImage(image, body_mask, region_mask):
    image = sitk.ReadImage(image)
    image = sitk.GetArrayFromImage(image)

    body = sitk.ReadImage(body_mask)
    body = sitk.GetArrayFromImage(body)

    if image.shape != body.shape:
        print("Body array not same shape")
        image = 0
        masked_image = 0
    
    else:
        mask = sitk.ReadImage(region_mask)
        mask = sitk.GetArrayFromImage(mask)

        if mask.shape != image.shape:
            print("Mask array not same shape")
            image = 0
            masked_image = 0
        
        else:
            if "glute" in region_mask:
                mask = mask / 13

            masked_image = ma.masked_array(image, mask = np.logical_not(mask), keep_mask = True, hard_mask = True)
            image = image.flatten()
            masked_image = masked_image.flatten()

    return image, masked_image


# patient directories
url = 'D://data//prostateMR_radiomics//nifti//SABR//0001088//'

# output
output = 'D:/data/Aaron/ProstateMRL/Data/MRLPacks/Histograms/'

ptDir = os.listdir(url)
print(ptDir)

for i in ptDir: 
    scans = os.listdir(url + str(i))

    for j in scans:
        print(str(j))
        glute_url = url + '/' + str(i) + '/' + '0001088_' + str(i) + '_glute.nii'
        pros_url = url + '/' + str(i) + '/' + '0001088_' + str(i) + '_shrunk_pros.nii'
        psoas_url = url + '/' + str(i) + '/' + '0001088_' + str(i) + '_psoas.nii'

        body_mask_url = url + '/' + str(i) + '/' + '0001088_' + str(i) + '_body_mask.nii'
        masks = [glute_url, pros_url, psoas_url]

        if "reg" in j:
            image_url =  url + '/' + str(i) + '/' + str(j)
            for k in masks:
                image = ReadImage(image_url, body_mask_url, k)[0]
                maskedimage = ReadImage(image_url, body_mask_url, k)[1]

                plt.hist(maskedimage, bins=512, range=(0,image.max()),alpha = 0.5, histtype = "step", fill = False, density = True, label = k)
                plt.hist(image, bins=512, range=(0,image.max()),alpha = 0.5, histtype = "step", fill = False, density = True, label = k)

            
            
            plt.savefig(output + "0001088"+str(i) + "_" + str(j)+ "_test.png", dpi=300)

        



