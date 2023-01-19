"""""

Aaron Rankin 08/03/22
Reads in matched nifti images, shrunk prostate contours and muscle clicks (outside dose field) 
and calculates mean and std
Saves to csv

"""""

import SimpleITK as sitk
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd

def MaskedImage(image_url, pros_url, glute_url, psoas_url):
    # read in image 
    image = sitk.ReadImage(image_url)
    image = sitk.GetArrayFromImage(image)
        
    mask_urls = [pros_url, glute_url, psoas_url]
    means = []
    for i in mask_urls:
        mask_url = i
        mask = sitk.ReadImage(mask_url)
        mask = sitk.GetArrayFromImage(mask)
        if "glute" in mask_url:
            mask = mask / 13
    
        if image.shape != mask.shape: # some images not same dimensions
            mean = np.nan
            means.append(mean)        
        else:
            masked_image = ma.masked_array(image, mask=np.logical_not(mask), keep_mask=True, hard_mask=True)
            mean = np.mean(masked_image.flatten())
            means.append(mean)

    return means  


patID = "1088"
patID_l = "0001088" # add extra 0 if 3 digit ID

url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_20f_new = 'D:/data/prostateMR_radiomics/nifti/20fractions_new/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
url_SABR_new = 'D:/data/prostateMR_radiomics/nifti/SABR_new/'

url = url_SABR + patID_l 
scanDir = os.listdir(url)

scan_info = pd.read_csv('D:/data/Aaron/ProstateMRL/Data/MRLPacks/ScanInfo/' + patID + '.csv')
scan_info = scan_info.dropna()

output = 'D:/data/Aaron/ProstateMRL/Data/MRLPacks/MeanValues/' 

print("Patient Directory: " + url)
print("Output Directory: " + output)

results_df = pd.DataFrame(columns=["PatID", "MRCont", "Fraction","ScanDate", "ScanTime", "Scan", "ProsMean", "GluteMean","PsoasMean","TimeDiff","ProsChange", "GluteChange", "PsoasChange"])
scanValues = {"PatID":[], "MRCont":[], "Fraction":[], "ScanDate":[], "ScanTime":[], "Scan":[], "ProsMean":[], "GluteMean":[],"PsoasMean":[], "TimeDiff":[], "ProsChange":[],"GluteChange":[], "PsoasChange":[]}

fractions = scan_info.Fraction.unique()
MRs = scan_info.MRContour.unique()

for i in fractions:
    MR = MRs[i].replace(' ', '')
    fraction = fractions[i]

    temp_df = scan_info.loc[scan_info['Fraction'] == fractions[i]] # get values for each fraction
    print('Pat: ' + patID + ' Fraction: ' + str(fraction) + ' MR: ' + MR)

    date = str(temp_df.ContourDate.unique()[0]) # all dates should be same for 1 fraction

    # add to dict prelim values
    scanValues["PatID"] = patID
    scanValues["MRCont"] = MR
    scanValues["Fraction"] = fraction
    scanValues["ScanDate"] = date

    scantimes = temp_df.ScanTime.unique() # get all different scantimes
    s = -1 # index for scantimes

    for j in os.scandir(url + '/' + MR):  # loop through files
        file = j.name
        glute_url = url + '/' + MR + '/' + patID_l + '_' + MR + '_glute.nii'
        pros_url = url + '/' + MR + '/' + patID_l + '_' + MR + '_shrunk_pros.nii'
        psoas_url = url + '/' + MR + '/' + patID_l + '_' + MR + '_psoas.nii'
        if "reg" in file:
            s = s + 1
            scan = file.split("_")
            scan = scan[4]
            scan = int(scan[0:1])
            scanValues["Scan"] = scan
            print("Scan: "+ str(scan))

            time = str(scantimes[s])
            time = time[0:7]
            scanValues["ScanTime"] = time

            DateTime = pd.to_datetime((date + time))

            image_url = url + '/' + MR + '/' + file
            means = MaskedImage(image_url, pros_url, glute_url, psoas_url)
            scanValues["ProsMean"] = means[0]
            scanValues["GluteMean"] = means[1]
            scanValues["PsoasMean"] = means[2]

            # get initial values for each fraction
            if scan == 1:
                datetime_1, pros_1, glute_1, psoas_1 = DateTime, means[0], means[1], means[2]
                scanValues["TimeDiff"] = 0
                scanValues["GluteChange"] = 0
                scanValues["ProsChange"] = 0
                scanValues["PsoasChange"] = 0

            else:
                scanValues["TimeDiff"] = DateTime - datetime_1
                scanValues["ProsChange"] = pros_1 - means[0]
                scanValues["GluteChange"] = glute_1 - means[1]
                scanValues["PsoasChange"] = psoas_1 - means[2]

            results_df = results_df.append(scanValues, ignore_index=True)
            
results_df.dropna()
results_df.to_csv(output + patID_l + ".csv")