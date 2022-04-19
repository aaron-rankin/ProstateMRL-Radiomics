"""""

Aaron Rankin 08/03/22
Reads in matched nifti images, shrunk prostate contours and muscle clicks (outside dose field) 
and calculates mean and std
Saves to csv

"""""

import fractions
from tempfile import tempdir
import SimpleITK as sitk
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd

patID = "1088"

url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_20f_new = 'D:/data/prostateMR_radiomics/nifti/20fractions_new/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
url_SABR_new = 'D:/data/prostateMR_radiomics/nifti/SABR_new/'

url = url_SABR + '000' + patID
scanDir = os.listdir(url)

scan_info = pd.read_csv('D:/data/Aaron/ProstateMRL/Data/MRLPacks/ScanInfo/' + patID + '.csv')

output = 'D:/data/Aaron/ProstateMRL/Data/Extraction/MRLPacks/MeanValues/' 

print("Patient Directory: " + url)
print("Output Directory: " + output)

print(scan_info.head())

for i in scanDir:
    niftis = os.scandir(url + '/' + str(i))
    print(i)

    temp_df = scan_info[scan_info['MRContour'].isin([i])]

    #print('Pat: ' + patID + ' Fraction: ' + str(frac) + ' MR: ' + str(i))

    print(temp_df.head)

    #for j in niftis:


