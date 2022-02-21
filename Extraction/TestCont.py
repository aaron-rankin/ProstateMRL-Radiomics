import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import csv

url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
ptDir = os.listdir(url_SABR)

#print(ptDir)

headings = ['Patient ID', 'Number of scans', 'Number of observers']

'''
with open('D:/data/prostateMR_radiomics/nifti/SABR_patients.csv', 'w', encoding='UTF8', newline='') as f:
    write_line = csv.writer(f)

    write_line.writerow(headings)
'''
for i in ptDir:
    scanWeeks = os.listdir(url_SABR + str(i))
    #print(scanWeeks)

    for j in scanWeeks:
       #print('Processing patient: ' + i + '   scan: ' + j)
       niftis = os.listdir(url_SABR + str(i) + "/" + str(j))
       
       imageName = url_SABR + str(i) + "/" + str(j)+"_NORMimage.nii"
       contours = []
       for k in niftis:
           
           if "ostate" in k:
               name = str(k)
               initials = name[9:11]
               #print(initials)
               contours.append(initials)

    print("Patient: " + str(i))           
    print("Number of contours: " + str(len(contours)))
    print("Number of scans: " + str(len(scanWeeks)))






