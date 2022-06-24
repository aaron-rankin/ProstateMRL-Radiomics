import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import pandas as pd

histmatch = True

csv_url = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\MeanValues\\"
packedIDs = os.listdir(csv_url)

# strip .csv
for p in range(len(packedIDs)):
    q = packedIDs[p]
    packedIDs[p] = q[:-4]

url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_SABR_new = 'D:/data/prostateMR_radiomics/nifti/SABR_new/'
url_SABR = 'D:/data/prostateMR_radiomics/nifti/SABR/'
url_20f_new = 'D:/data/prostateMR_radiomics/nifti/20fractions_new/'

url = url_20f

ptDir = os.listdir(url)

print(packedIDs)
print(ptDir)

#packedIDs = ["0000653", "0000826"]
#plt.figure('Histograms')
packedIDs = ["312108"]
for i in ptDir:
	patID_s = i#lstrip("0000")

	if patID_s in packedIDs:
            pat_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\ScanInfo\\" + i + ".csv")
            MRcont = pat_df.MRContour.unique()
            print(MRcont)
            scans = os.listdir(url + str(i))

            #sorted_scans = [elem.replace("MR", "")for elem in scans]
            #sorted_scans = [int(p) for p in sorted_scans]
            first_scan = MRcont[0]
            first_scan = first_scan[1:]
            print(first_scan)
            #print("First scan: " + str(first_scan))
            
            #refPat = url + i + "\\" + str(first_scan) + '\\' + "BaseImages" + "\\" + i + "_" + str(first_scan) + "_image.nii"
            refPat = 'D:/data/prostateMR_radiomics/nifti/SABR/0001307/MR6/BaseImages/0001307_MR6_image.nii' # if HM2 - ref scan is first scan per patient
            
            refimage =  sitk.ReadImage(refPat) 
            result = sitk.GetArrayFromImage(refimage)
            result = result.flatten()
            refmax = result.max()
            
            for j in MRcont:
                    print('Processing patient: ' + i + '   scan: ' + j)

                    image = sitk.ReadImage(url + str(i) + '/' + str(j)[1:] + '/BaseImages/' + str(i) + "_" + j[1:] + "_image.nii")
                    image = sitk.ReadImage(url + str(i) + '/' + str(j)[1:] + '/BaseImages/' + str(i) + "_" + j[1:] + "_image.nii")
                    matcher = sitk.HistogramMatchingImageFilter()
                    matcher.SetNumberOfHistogramLevels(1024)
                    matcher.SetNumberOfMatchPoints(25)
                    matcher.ThresholdAtMeanIntensityOn()
                    image = matcher.Execute(image, refimage)
                    sitk.WriteImage(image,url + i + '/' + j[1:] + '/HM-TP/' + i + '_' + j[1:] + '_HM-TP_test_.nii' )
