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

url = url_SABR

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
                mask = url + str(i) + "\\" + str(j) + "\\" + str(k)
                readMask = sitk.ReadImage(mask)
                mask = readMask
                omaskorigin = mask.GetOrigin()
                omaskspacing = mask.GetSpacing()
                omaskdirection = mask.GetDirection()
                print(omaskorigin, omaskspacing, omaskdirection)
                newMaskArray = sitk.GetArrayFromImage(mask)
                dilateMaskArray = newMaskArray.copy()
                dilateMaskArray == 1

                structExample = generate_binary_structure(3, 3)  
                dilateMaskArray = binary_dilation(dilateMaskArray, structExample, iterations = 10) #edit number of iterations to make sure all gaps in mask are being filled
                erodeMaskArray = binary_erosion(dilateMaskArray, structExample, iterations = 13)
                newMaskArray[:,:,:] = 0
                newMaskArray[np.where(erodeMaskArray == True)] = 1
                erodedMask = sitk.GetImageFromArray(newMaskArray)

                erodedMask.SetOrigin(omaskorigin)
                erodedMask.SetSpacing(omaskspacing)
                erodedMask.SetDirection(omaskdirection)

                maskorigin = erodedMask.GetOrigin() 
                maskspacing = erodedMask.GetSpacing()
                maskdirection = erodedMask.GetDirection()
                print(maskorigin, maskspacing, maskdirection)
                
                

                sitk.WriteImage(erodedMask, url + i + '/' + j + '/' + i + '_' + j + '_body_mask.nii' )
                
