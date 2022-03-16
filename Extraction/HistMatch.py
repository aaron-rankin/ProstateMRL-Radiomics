import SimpleITK as sitk
import numpy as np
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os

histmatch = True

url_20f = 'D:/data/prostateMR_radiomics/nifti/20fractions/'
url_SABR = 'D:/data/prostateMR_radiomics/patientData/nifti_new/new_SABR/'
ptDir = os.listdir(url_20f)

url = url_20f
# if histmatch:
#     refPat = 'D:/data/prostateMR_radiomics/nifti/20fractions/0000213/MR4/0000213_MR4_image.nii' 
#     refimage =  sitk.ReadImage(refPat) 
#     result = sitk.GetArrayFromImage(refimage)
# 	#plt.figure('reference histogram')
#     result = result.flatten()
#     refmax = result.max()
    #print(refmax)

    #plt.hist(result, bins=64, range= (1,refmax),facecolor='red', alpha=0.75,histtype = 'step', density=True)
    #plt.xlabel('MR intensity')
    #plt.ylabel('Percentage') 
    #plt.savefig('D:/data/prostateMR_radiomics/patientData/nifti_new/normalisation' + 'ref.png', dpi=300)


#plt.figure('Histograms')
for i in ptDir:
	scans = os.listdir(url_20f + str(i))

	sorted_scans = [elem.replace("MR", "")for elem in scans]
	sorted_scans = [int(p) for p in sorted_scans]
	first_scan = min(sorted_scans)
	
	refPat = 'D:/data/prostateMR_radiomics/nifti/20fractions/0000213/MR4/0000213_MR4_image.nii' # if HM1 - one ref scan all group
	#refPat = url + i + "/" + "MR" + str(first_scan) + '/' + i + "_MR" + str(first_scan) + "_image.nii" # if HM2 - ref scan is first scan per patient
	
	refimage =  sitk.ReadImage(refPat) 
	result = sitk.GetArrayFromImage(refimage)
	result = result.flatten()
	refmax = result.max()
	
	for j in scans:
		print('Processing patient: ' + i + '   scan: ' + j)

		image = sitk.ReadImage(url_20f + i + '/' + j + '/' + i + '_' + j + '_image.nii')
		
		matcher = sitk.HistogramMatchingImageFilter()
		matcher.SetNumberOfHistogramLevels(1024)
		matcher.SetNumberOfMatchPoints(25)
		matcher.ThresholdAtMeanIntensityOn()
		image = matcher.Execute(image, refimage)
		sitk.WriteImage(image, url_20f + i + '/' + j + '/' + i + '_' + j + '_HM1_image.nii' )
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