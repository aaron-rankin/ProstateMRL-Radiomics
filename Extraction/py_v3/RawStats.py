from pydoc import pathdirs
import SimpleITK as sitk
from matplotlib.pyplot import contour
import numpy as np
import pandas as pd
import os
import UsefulFunctions as UF
import ImageFunctions as IF
from datetime import datetime
import radiomics
print(radiomics.__version__)
from radiomics import featureextractor

key_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\All_PatientKey.csv")

url = "D:\\data\\prostateMR_radiomics\\nifti\\"
output_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\RawStats\\"

parameters = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\ExtractionParams\\RawStats.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(parameters)

all_df = pd.DataFrame()
col_names = ["PatID","Treatment","Scan","DaysDiff","Normalisation","Region","Mean","Median", "Std", "10Perc", "90Perc", "Volume"]

t_dir = key_df.FileDir.unique()

for t in t_dir:
   t_df = key_df.loc[key_df["FileDir"] == t]
   patIDs = t_df.PatID.unique()

   print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   print("Treatment: {}".format(t))
   print("Patients: {}".format(patIDs))
   for i in patIDs:
        patID = UF.FixPatID(i, t) # use i for accessing key df, patID for roots to files

        pat_df = t_df[t_df["PatID"].isin([i])]

        scans = pat_df.Scan.unique()
        print("####################################################")
        print("Patient: {}".format(patID))
        
        dates = pat_df.Date.unique()

        first_date = dates[0]
        first_date = UF.FixDate(first_date)      
        
        p_vals_df = pd.DataFrame()

        for MRscan in scans:
            MRscan = MRscan 
            pat_path = os.path.join(url, t, patID, MRscan)

            scan_df = pat_df.loc[pat_df["Scan"] == (MRscan)]
            scan_date = str(scan_df.iloc[0]["Date"])
            scan_date = UF.FixDate(scan_date)
            days_diff = (scan_date - first_date).days

            print("Scan: {}".format(MRscan))

            mask_path, mask_labels, image_paths, image_labels = UF.GetNiftiPaths(pat_path, t)
            image_paths = [image_paths[0]]

            folder, label = image_paths[0], "Raw"
            image_path, image_name = UF.GetImageFile(folder, patID, MRscan, label)

            norm = UF.GetNorm(image_name)

            for m in mask_labels:
                values = {}
                region = UF.GetRegion(m)

                mask_file = patID + "_" + MRscan + m 
                mask_file_path = os.path.join(mask_path, mask_file)
                mask_value = IF.MaskValue(m)
   
                temp_results = pd.DataFrame()
                temp_results = pd.Series(extractor.execute(image_path, mask_file_path, label=mask_value))
                temp_trans = temp_results.iloc[22:]
                
                values["PatID"], values["Treatment"], values["Scan"], values["DaysDiff"] = patID, t, MRscan, int(days_diff)
                values["Normalisation"], values["Region"] = norm, region
                values["Mean"], values["Median"] = temp_trans.iloc[1], temp_trans.iloc[2]
                values["Std"], values["10Perc"], values["90Perc"] = np.sqrt(temp_trans.iloc[5]), temp_trans.iloc[3], temp_trans.iloc[4]
                values["Volume"] = temp_trans.iloc[0]

                p_vals_df = p_vals_df.append(values, ignore_index = True)

        p_vals_df = p_vals_df[col_names]
        p_vals_df.to_csv(output_dir + "\\" + t + "_" + patID + "_RawStats.csv")
            
       