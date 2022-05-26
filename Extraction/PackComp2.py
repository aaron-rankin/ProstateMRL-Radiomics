"""""

Aaron Rankin 08/03/22
Reads in matched nifti images, shrunk prostate contours and muscle clicks (outside dose field) 
and calculates mean and std
Saves to csv

"""""

import SimpleITK as sitk
import numpy as np
import numpy.ma as ma
import os
import sys
import pandas as pd

def MaskedImage(image_url, mask_url):
    # read in image 
    image = sitk.ReadImage(image_url)
    image_array = sitk.GetArrayFromImage(image)
        
    mask = sitk.ReadImage(mask_url)
    mask_array = sitk.GetArrayFromImage(mask) 
    if "glute" in mask_url:
        mask_array = mask_array / 13
    
    if image_array.shape != mask_array.shape:
        mean = np.nan
        std = np.nan
    
    else:
        masked_image = ma.masked_array(image_array, mask=np.logical_not(mask_array), keep_mask=True, hard_mask=True)
        mean = np.mean(masked_image.flatten())
        std = np.std(masked_image.flatten())

    return mean 
    


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

results_df = pd.DataFrame(columns=["PatID", "MRCont", "Fraction","ScanDate", "ScanTime", "Scan", "Region", "MeanSignal", "TimeDiff","SignalChange"])
scanValues = {"PatID":[], "MRCont":[], "Fraction":[], "ScanDate":[], "ScanTime":[], "Scan":[], "Region":[], "MeanSignal":[], "TimeDiff":[], "SignalChange":[]}

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

        mask_urls = [pros_url, glute_url, psoas_url]

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

            for k in range(len(mask_urls)):
                mean = MaskedImage(image_url, mask_urls[k])
                scanValues["MeanSignal"] = mean

                if k == 0:
                    scanValues["Region"] = "Prostate"
                    if scan == 1:
                        pros_firstmean, datetime_1 = mean, DateTime
                        scanValues["SignalChange"] = 0 
                        scanValues["TimeDiff"] = 0
                    else:
                        scanValues["SignalChange"] = mean - pros_firstmean
                        scanValues["TimeDiff"] = DateTime - datetime_1
                elif k == 1:
                    scanValues["Region"] = "Glute"
                    if scan == 1:
                        glute_firstmean, datetime_1 = mean, DateTime
                        scanValues["SignalChange"] = 0 
                        scanValues["TimeDiff"] = 0
                    else:
                        scanValues["SignalChange"] = mean - glute_firstmean
                        scanValues["TimeDiff"] = DateTime - datetime_1
                elif k == 2:
                    scanValues["Region"] = "Psoas"
                    if scan == 1:
                        psoas_firstmean, datetime_1 = mean, DateTime
                        scanValues["SignalChange"] = 0 
                        scanValues["TimeDiff"] = 0
                    else:
                        scanValues["SignalChange"] = mean - psoas_firstmean
                        scanValues["TimeDiff"] = DateTime - datetime_1
                
                results_df = results_df.append(scanValues, ignore_index=True)


results_df.dropna()



print("---------------Done----------------")
results_df.to_csv(output + patID_l + ".csv")