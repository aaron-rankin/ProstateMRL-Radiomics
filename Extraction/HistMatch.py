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

url = url_SABR

ptDir = os.listdir(url)


# if histmatch:
#refPat = 'D:/data/prostateMR_radiomics/nifti/SABR/0001307/MR6/Reg-Raw/0001307_MR6_reg_img_1.nii' 
#refimage =  sitk.ReadImage(refPat) 
#result = sitk.GetArrayFromImage(refimage)
# 	#plt.figure('reference histogram')
#     result = result.flatten()
#     refmax = result.max()
    #print(refmax)

    #plt.hist(result, bins=64, range= (1,refmax),facecolor='red', alpha=0.75,histtype = 'step', density=True)
    #plt.xlabel('MR intensity')
    #plt.ylabel('Percentage') 
    #plt.savefig('D:/data/prostateMR_radiomics/patientData/nifti_new/normalisation' + 'ref.png', dpi=300)

packedIDs = ["0000653", "0000826"]
#plt.figure('Histograms')
for i in ptDir:
	patID_s = i

	if patID_s in packedIDs:
		pat_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\ScanInfo\\" + i + ".csv")
		MRcont = pat_df.MRContour.unique()
		scans = os.listdir(url + str(i))

		#sorted_scans = [elem.replace("MR", "")for elem in scans]
		#sorted_scans = [int(p) for p in sorted_scans]
		first_scan = MRcont[0]
		first_scan = first_scan[1:]
		print("First scan: " + str(first_scan))
		
		#refPat = 'D:/data/prostateMR_radiomics/nifti/20fractions/0000213/MR4/0000213_MR4_image.nii' # if HM1 - one ref scan all group
		refPat = url + i + "\\" + str(first_scan) + '\\' + "Reg-Raw" + "\\" + i + "_" + str(first_scan) + "_reg_img_1.nii" # if HM2 - ref scan is first scan per patient
		
		refimage =  sitk.ReadImage(refPat) 
		result = sitk.GetArrayFromImage(refimage)
		result = result.flatten()
		refmax = result.max()
		
		for j in MRcont:
			#print('Processing patient: ' + i + '   scan: ' + j)
			reg_imgs = os.listdir(url + str(i) + '/' + str(j)[1:] + '/Reg-Raw/')

			for k in reg_imgs: 
				scan_num = int(k[-5:-4])
				print('Processing patient: ' + i + '   scan: ' + j[1:] + ' Scan: ' + str(scan_num))

				image = sitk.ReadImage(url + str(i) + '/' + str(j)[1:] + '/Reg-Raw/' + str(k))
				
				matcher = sitk.HistogramMatchingImageFilter()
				matcher.SetNumberOfHistogramLevels(1024)
				matcher.SetNumberOfMatchPoints(25)
				matcher.ThresholdAtMeanIntensityOn()
				image = matcher.Execute(image, refimage)
				sitk.WriteImage(image,url + i + '/' + j[1:] + '/HM-FS/' + i + '_' + j[1:] + '_HM-FS_' + str(scan_num) + '_.nii' )
#		result = sitk.GetArrayFromImage(image)

#		if not histmatch:
#			refmax = result.max()

#		result = result.flatten()
#		plt.hist(result, bins=64, range= (1,refmax),facecolor='red', alpha=0.75,histtype = 'step', density=True)
#		plt.xlabel('MR intensity')
#		plt.ylabel('Percentage')

#		if histmatch:
#			plt.savefig('D:/data/prostateMR_radiomics/new_Histograms/new_20fractions/normHistograms/' + '/' + i + '_' + j + '.png', dpi=300)
#		else:        
#			plt.savefig('D:/data/prostateMR_radiomics/new_Histograms/new_20fractions/rawHistograms' + '/' + i + '_' + j + '.png', dpi=300)
		#plt.show()