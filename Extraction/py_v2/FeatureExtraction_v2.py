from pydoc import pathdirs
import SimpleITK as sitk
from matplotlib.pyplot import contour
import numpy as np
import pandas as pd
import os
import UsefulFunctions as UF
from datetime import datetime
import radiomics
print(radiomics.__version__)
from radiomics import featureextractor

paramPath = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\ExtractionParams\\Run1.yaml"
output_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\FeatureExtraction\\"

scans_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\PatientKey_sorted.csv")
treatments = ["SABR"] # "20fractions"

url = "D:\\data\\prostateMR_radiomics\\nifti\\"

all_df = pd.DataFrame()

extractor = featureextractor.RadiomicsFeatureExtractor(paramPath)


for t in treatments:
    t_df = scans_df.loc[scans_df["Treatment"] == t]
    patIDs = t_df.Patient.unique()
    print(patIDs)
    

    for i in patIDs:
        # read in pat csv
        pat_df = t_df[t_df["Patient"].isin([i])]
        i = UF.FixPatID(i)
        patID = i 
        scans = pat_df.Scan.unique()

        if patID == "0001464" and t == "SABR":
            patID_l = patID + "_" + t
        elif patID == "0001464" and t == "20fractions":
            patID_l = patID + "_" + "20f"
        
        for j in scans:
            MRcont = j
            pat_path = url + str(t) + "\\" + str(i) + "\\" + MRcont + "\\"

            scan_df = pat_df.loc[pat_df["Scan"] == (MRcont)] 

            scan_date = str(scan_df.iloc[0]["DateofScan"])
           
            if len(scan_date) != 8:
                scan_date = scan_date[:-2]
            scan_date = (datetime.strptime(str(scan_date), "%Y%m%d")).date()
           

            print("Patient: {} | Scan: {}".format(patID, MRcont))
            
            # Generate paths
            pat_path = os.path.join(url, t, patID, MRcont)

            mask_url = os.path.join(pat_path, "Masks\\" + patID + "_" + j + "_shrunk_pros.nii")

            raw_path = os.path.join(pat_path, "BaseImages\\")
            norm_pros_path = os.path.join(pat_path, "Norm-Pros\\")
            norm_psoas_path = os.path.join(pat_path, "Norm-Psoas\\")
            norm_glute_path = os.path.join(pat_path, "Norm-Glute\\")
            med_pros_path = os.path.join(pat_path, "Med-Pros\\")
            med_psoas_path = os.path.join(pat_path, "Med-Psoas\\")
            med_glute_path = os.path.join(pat_path, "Med-Glute\\")
            HM_TP_path = os.path.join(pat_path, "HM-TP\\")
            HM_FS_path = os.path.join(pat_path, "HM-FS\\")

            image_paths = [raw_path, norm_glute_path, med_glute_path,norm_pros_path, med_pros_path,norm_psoas_path, med_psoas_path,HM_FS_path, HM_TP_path] #med_pros_path,  med_psoas_path, med_glute_path, 
            
            for k in image_paths:
                images = os.listdir(os.path.join(pat_path,k))

                # folder empty if haven't done norm
                if len(images) != 0:

                    # only want first scan (inter-fraction changes)    

                    if k == raw_path:
                        image_name = str(i) + "_" + MRcont + "_image.nii"  
                        norm = "Raw"

                    if "HM" in k:
                        image_name = images[0]
                        norm = UF.GetNorm(image_name)

                    else:
                        image_name = images[-1]
                        norm = UF.GetNorm(image_name)
                        
                    image_url = os.path.join(k,image_name)

                    tmpResults = pd.DataFrame()
                    tempProstate = pd.Series(extractor.execute(image_url, mask_url))
                    tempProstate.name = patID + "_" + j + "_" + norm
                    tmpResults = tmpResults.append(tempProstate)
                    print("Patient: " + tempProstate.name)
                    
                    pat_folder = output_dir + patID
                    if patID == "0001464":
                        pat_folder = output_dir + patID_l
                    if os.path.exists(pat_folder):	
                        print()
                    else:
                        os.mkdir(pat_folder)
                    if patID == "0001464":
                        output_folder = output_dir + patID_l + "\\" + str(j)
                    else:
                        output_folder = output_dir + str(i) + "\\" + str(j)
                    if os.path.exists(output_folder):
                        print()
                    else:
                        os.mkdir(output_folder)
                    
                    tmpResults.to_csv(output_folder + "\\" + tempProstate.name + "_features.csv")
                    print("--------------------")  




