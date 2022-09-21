from pydoc import pathdirs
import SimpleITK as sitk
from matplotlib.pyplot import contour
import numpy as np
import pandas as pd
import os
import UsefulFunctions as UF
from datetime import datetime
import radiomics
from radiomics import featureextractor

root = UF.DataRoot()

key_df = pd.read_csv(os.path.join(root, "Aaron\\ProstateMRL\\Data\\PatientKey_sorted.csv"))
nifti_dir = os.path.join(root, "prostateMR_radiomics\\nifti\\")
output_dir = os.path.join(root, "Aaron\\ProstateMRL\\Data\\MRLPacks\\Features_v2\\")

parameters = root + "Aaron\\ProstateMRL\\Data\\MRLPacks\\ExtractionParams\\Run1.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(parameters)

all_df = pd.DataFrame()
col_names = ["PatID","Treatment","Scan","DaysDiff","Normalisation","Region","Mean","Median", "Std", "10Perc", "90Perc"]
key_df.drop(["Unnamed: 0"], axis=1, inplace=True)
treatments = ["SABR","20fractions"]

for t in treatments: 
    t_df = key_df.loc[key_df["Treatment"] == t]
    patIDs = t_df.Patient.unique()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Treatment: {}".format(t))
    print("Patients: {}".format(patIDs))

    for i in patIDs:
        pat_df = t_df[t_df["Patient"].isin([i])]
        patID = UF.FixPatID(i)
        scans = pat_df.Scan.unique()
        print("####################################################")
        print("Patient: {}".format(patID))
       
        dates = pat_df.DateofScan.unique()

        first_date = dates[0]
        first_date = UF.FixDate(first_date)      
        
        p_df = pd.DataFrame()

        for j in scans:
            MRcont = j 
            pat_path = os.path.join(nifti_dir, t, patID, MRcont)

            scan_df = pat_df.loc[pat_df["Scan"] == (MRcont)]
            scan_date = str(scan_df.iloc[0]["DateofScan"])
            scan_date = UF.FixDate(scan_date)
            days_diff = (scan_date - first_date).days

            print("Scan: {}".format(MRcont))


            mask_path, mask_labels, image_paths, image_labels = UF.GetNiftiPaths(pat_path, t)


            for k in range(len(image_paths)):
        
                folder = image_paths[k]
                label = image_labels[k]
                
                image_path, image_name = UF.GetImageFile(folder, patID, MRcont, label)

                norm = UF.GetNorm(image_name)


                for m in mask_labels:
                    values = {}
                    region = UF.GetRegion(m)
                    
                    mask_file = patID + "_" + MRcont + m 
                    mask_file_path = os.path.join(mask_path, mask_file)
                    mask_value = UF.MaskValue(m)
                    
                    temp_df = pd.DataFrame()
                    temp_results = pd.Series(extractor.execute(image_path, mask_file_path, label=mask_value))
                    temp_df = temp_df.append(temp_results, ignore_index=True)
                   
                    temp_df.insert(0, "PatID", patID)
                    temp_df.insert(1, "Treatment", t)
                    temp_df.insert(2, "Scan", MRcont)
                    temp_df.insert(3, "DaysDiff", int(days_diff))
                    temp_df.insert(4, "Normalisation", norm)
                    temp_df.insert(5, "Region", region)

                    p_df = p_df.append(temp_df, ignore_index=True)
                                       

        all_df = all_df.append(p_df, ignore_index=True)
        p_df.to_csv(output_dir + t + "_" + patID + "_pyRad_Features.csv")

               

all_df.to_csv(output_dir + "All_pyRad_Features.csv")
            
