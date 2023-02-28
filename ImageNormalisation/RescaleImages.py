import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
import sys
from radiomics import featureextractor

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF


root = UF.DataRoot(2)
nifti_dir = root + "\\prostateMR_radiomics\\nifti\\"
# Get patkey
PatKey = pd.read_csv(root + "Aaron\ProstateMRL\Code\PatKeys\\AllPatientKey_s.csv")
Extraction = True
e_params = root + "Aaron\\ProstateMRL\Code\Features\\Parameters\\MedianSignal.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(e_params)

masks = ["Pros", "glute", "psoas"]

PatIDs = PatKey["PatID"].unique()


def CalcSignal(ImagePath, MaskPath, MaskValue):
    # Get image
    temp_df = pd.DataFrame()
    temp_res = pd.Series(extractor.execute(ImagePath, MaskPath, MaskValue))
    temp_df = temp_df.append(temp_res, ignore_index=True)

    return temp_df

for PatID in PatIDs:

    pat_key = PatKey[PatKey["PatID"] == PatID]
    dir = pat_key["FileDir"].values[0]

    PatID = UF.FixPatID(PatID, dir)
    Scans = pat_key["Scan"].unique()

    for Scan in Scans:
        print(PatID, Scan)

        if Extraction == True:

            for Mask in masks:
                if Mask == "Pros":
                    Mask = "shrunk_pros"


                ImagePath = os.path.join(nifti_dir, dir, PatID, Scan, "Raw\\", PatID + "_" + Scan + "_Raw.nii")
                MaskPath = os.path.join(nifti_dir, dir, PatID, Scan, "Mask\\", PatID + "_" + Scan + "_" + Mask + ".nii")
                MaskValue = IF.MaskValue(Mask)

                temp_df = CalcSignal(ImagePath, MaskPath, MaskValue)
                print(temp_df)








            


                

                
                    





