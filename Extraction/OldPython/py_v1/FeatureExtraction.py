
import os
import six
import radiomics
import pandas as pd
print(radiomics.__version__)
from radiomics import featureextractor

paramPath = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\ExtractionParams\\Run1.yaml"
output_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\FeatureExtraction\\"

scaninfo_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges\\"
packedIDs = os.listdir(scaninfo_dir)

for p in range(len(packedIDs)):
    q = packedIDs[p]
    packedIDs[p] = q[:-10]

# set patient directory
url_SABR = "D:\\data\\prostateMR_radiomics\\nifti\\SABR\\"
url_20f = "D:\\data\\prostateMR_radiomics\\nifti\\20fractions\\"

url = url_20f

ptDir = os.listdir(url)
print(packedIDs)
print(ptDir)

extractor = featureextractor.RadiomicsFeatureExtractor(paramPath)

for i in ptDir:
	patID = i
	if i in packedIDs:

		pat_df = pd.read_csv(scaninfo_dir + patID + "_inter.csv")

		MRcontours = pat_df.MRContour.unique()
		
		for j in MRcontours:
			pat_path = os.path.join(url, patID, j)
			MRcont = j
		
			mask_url = os.path.join(pat_path, "Masks\\" + patID + "_" + j + "_shrunk_pros.nii")
			
			raw_path = os.path.join(pat_path, "BaseImages\\")
			norm_pros_path = os.path.join(pat_path, "Norm-Pros\\")
			norm_psoas_path = os.path.join(pat_path, "Norm-Psoas\\")
			norm_glute_path = os.path.join(pat_path, "Norm-Glute\\")
			HM_TP_path = os.path.join(pat_path, "HM-TP\\")
			HM_FS_path = os.path.join(pat_path, "HM-FS\\")

			image_paths = [raw_path, norm_glute_path, norm_pros_path, norm_psoas_path, HM_FS_path, HM_TP_path]
			
			for k in image_paths:
				images = os.listdir(k)

				# folder empty if haven't done norm
				if len(images) != 0:

					# only want first scan (inter-fraction changes)    

					if "BaseImages" in k:
						image_name = str(i) + "_" + MRcont + "_image.nii"  
						norm = "Raw"

					else:
						image_name = images[-1]
						norm = image_name.split("_")[2]
						
					image_url = os.path.join(k,image_name)

					tmpResults = pd.DataFrame()	
					tempProstate = pd.Series(extractor.execute(image_url, mask_url))
					
					tempProstate.name = patID + "_" + j + "_" + norm
					tmpResults = tmpResults.append(tempProstate)
					print("Patient: " + tempProstate.name)


					pat_folder = output_dir + str(i)
					if os.path.exists(pat_folder):	
						print()
					else:
						os.mkdir(pat_folder)
					
					output_folder = output_dir + str(i) + "\\" + str(j)
					if os.path.exists(output_folder):	
						print()
					else:
						os.mkdir(output_folder)

					tmpResults.to_csv(output_folder + "\\" + tempProstate.name + "_features.csv")
		print("--------------------")

