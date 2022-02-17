
import os
import six
import radiomics
import pandas

print(radiomics.__version__)
from radiomics import featureextractor

paramPath = "D:\\data\\prostateMR_radiomics\Params.yaml"

ptDir = os.listdir("D:\\data\\prostateMR_radiomics\\patientData\\nifti_new\\new_SABR\\")
#print (ptDir)

extractor = featureextractor.RadiomicsFeatureExtractor(paramPath)

for i in ptDir:
	scanWeeks = os.listdir("D:\\data\\prostateMR_radiomics\\patientData\\nifti_new\\new_SABR\\"+str(i))
	
	for j in scanWeeks:
		niiFiles = os.listdir("D:\\data\\prostateMR_radiomics\\patientData\\nifti_new\\new_SABR\\"+str(i)+"\\"+str(j))
		# print(niiFiles)
		print ("Processing: "+i+"  Timepoint: "+j)	
		imageName = "D:\\data\\prostateMR_radiomics\\patientData\\nifti_new\\new_SABR\\"+str(i)+"\\"+str(j)+"\\"+str(i)+"_"+str(j)+"_NORMimage.nii"
		#print ("image  "+imageName)

		#for k in niiFiles:
		tmpResults = pandas.DataFrame()	
		#print(j)

		for k in niiFiles:
			x = "ostate"
			y = "RP"
			if y in k:
			#if x in k:
			
				name = str(k)
				name_size = len(str(k))
				initials = name[9:11]
			#	print("Image: " + imageName, ", " + j)
				segmentation = True
				#print(k)
				maskName = "D:\\data\\prostateMR_radiomics\\patientData\\nifti_new\\new_SABR\\"+str(i)+"\\"+str(j)+"\\"+str(k)
				#print("Mask: " + maskName)
				#print("Image: " + imageName)
				tempProstate = pandas.Series(extractor.execute(imageName, maskName))
				
				tempProstate.name = name[:name_size - 4]
				tmpResults = tmpResults.append(tempProstate)
				#print(tempProstate.name)
				
				#print(initials)
			else:
				segmentation = False
			
		if segmentation == False:
			print ("Check segmentation list for "+j)
		

		output_folder = "D:\\data\\prostateMR_radiomics\\prostateMR_radiomics_new\\SABR_new\\"+str(i)
		if not os.path.exists(output_folder):	
			os.mkdir(output_folder)
		else:
			print()
		tmpResults.T.to_csv("D:\\data\\prostateMR_radiomics\\prostateMR_radiomics_new\\SABR_new\\"+str(i)+"\\"+str(i)+"_"+str(j) + ".csv")

