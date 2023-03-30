import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
import sys
from radiomics import featureextractor
from tqdm import tqdm

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF


root = UF.DataRoot(1)
nifti_dir = root + "\\prostateMR_radiomics\\nifti\\"
# Get patkey
PatKey = pd.read_csv(root + "Aaron\ProstateMRL\Code\PatKeys\\AllPatientKey_s.csv")
Extraction = True
e_params = root + "Aaron\\ProstateMRL\Code\Features\\Parameters\\MedianSignal.yaml"
extractor = featureextractor.RadiomicsFeatureExtractor(e_params)

masks = ["Pros", "psoas"]
PatKey = PatKey.loc[PatKey["Treatment"] == "SABR"]
PatIDs = PatKey["PatID"].unique()

Signal_df = pd.DataFrame()

Norms = ["Raw", "HM-FS", "HM-TP", "HM-FSTP", "Med-Pros", "Med-Psoas"]
for Norm in Norms:
    for PatID in tqdm(PatIDs):

        pat_key = PatKey[PatKey["PatID"] == PatID]
        t_dir = pat_key["FileDir"].values[0]

        PatID = UF.FixPatID(PatID, t_dir)
        Scans = pat_key["Scan"].unique()

        for Scan in Scans:

            for Mask in masks:
                if Mask == "Pros":
                    Mask = "shrunk_pros"

                ImageFile = PatID + "_" + Scan + "_Raw.nii"
                MaskFile = PatID + "_" + Scan + "_" + Mask + ".nii"
                ImagePath = os.path.join(nifti_dir, t_dir, PatID, Scan, Norm, ImageFile)
                MaskPath = os.path.join(nifti_dir, t_dir, PatID, Scan, "Masks\\", MaskFile)
                Median = IF.MaskedMeanMed(ImagePath, MaskPath)[1]

                data = [[PatID, Norm, Scan, Mask, Median]]
                temp_df = pd.DataFrame(data, columns = ["PatID", "Norm", "Scan", "Mask", "Median"])
                
                Signal_df = Signal_df.append(temp_df, ignore_index=True)

Signal_df.to_csv(root + "Aaron\ProstateMRL\Code\PatKeys\\MedianSignalNorm.csv")
                
        









            


                

                
                    





