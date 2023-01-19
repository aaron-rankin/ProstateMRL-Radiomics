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
from radiomics import featureextractor

root = "D:\\data\\"

key_df = pd.read_csv(os.path.join(root, "Aaron\\ProstateMRL\\Data\\MRLPacks\\All_PatientKey.csv"))
nifti_dir = os.path.join(root, "prostateMR_radiomics\\nifti\\")
output_dir = os.path.join(root, "Aaron\\ProstateMRL\\Data\\MRLPacks\\AutoContouringVol\\")

parameters = root + "Aaron\\ProstateMRL\\Data\\MRLPacks\\ExtractionParams\\Volume.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(parameters)

t_dir = key_df.FileDir.unique()
t_dir = t_dir[2:3]

for t in t_dir: 
    t_df = key_df.loc[key_df["FileDir"] == t]
    patIDs = t_df.PatID.unique()[5:]
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Treatment: {}".format(t))
    print("Patients: {}".format(patIDs))

    for i in patIDs:
            pat_df = t_df[t_df["PatID"].isin([i])]
            patID = UF.FixPatID(i,t)
            scans = pat_df.Scan.unique()
            print("####################################################")
            print("Patient: {}".format(patID))
                
            p_df = pd.DataFrame()

            for j in range(len(scans)):
                MRcont = scans[j] 
                pat_path = os.path.join(nifti_dir, t, patID, MRcont)

                scan_df = pat_df.loc[pat_df["Scan"] == (MRcont)]

                print("Scan: {}".format(MRcont))

                mask_path, mask_labels, image_paths, image_labels = UF.GetNiftiPaths(pat_path, t)
                image_path = image_paths[0]
                image_name = patID + "_" + MRcont + "_Raw.nii"

                RP = mask_path + patID + "_" + MRcont + "_Prostate_RP.nii"
                #Admire = mask_path + patID + "_" + MRcont + "_Admire.nii"
                Limbus = root + "prostateMR_radiomics\\PatPacks\\LimbusMasks\\" + t + "_" + patID + "_" + str(j+1) + "_Limbus.nii"
                
                mask_paths = [RP, Limbus]
                mask_labels = ["Manual", "Limbus"]
                
                for k in range(len(mask_paths)):
            
                    image = image_path + image_name
                    mask = mask_paths[k]
                    values = {}
                    
                    if k == 1:
                        mask_value = 255
                    else:
                        mask_value = 1
                    
                    #print(mask, k, mask_value)

                    temp_df = pd.DataFrame()
                    temp_results = pd.Series(extractor.execute(image, mask, label=mask_value))
                    temp_df = temp_df.append(temp_results, ignore_index=True)
                     
                    temp_df.insert(0, "PatID", patID)
                    temp_df.insert(1, "Treatment", t)
                    temp_df.insert(2, "Scan", MRcont)
                    temp_df.insert(3, "Mask", mask_labels[k])
                    
                    p_df = p_df.append(temp_df, ignore_index=True)
                                        
            p_df = p_df.drop(p_df.columns[4:-1], axis=1)
            p_df.to_csv(output_dir + t + "_" + patID  + "_ContourVol.csv")
