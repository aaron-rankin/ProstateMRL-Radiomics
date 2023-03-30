import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
import sys
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

masks = ["Pros", "psoas"]
PatKey = PatKey.loc[PatKey["Treatment"] == "SABR"]
PatIDs = PatKey["PatID"].unique()

Signal_df = pd.read_csv(root + "Aaron\ProstateMRL\Code\PatKeys\\MedianSignal.csv")

for PatID in tqdm(PatIDs):

    pat_key = PatKey[PatKey["PatID"] == PatID]
    Pat_df = Signal_df.loc[Signal_df["PatID"] == PatID]
    t_dir = pat_key["FileDir"].values[0]

    PatID = UF.FixPatID(PatID, t_dir)
    Scans = pat_key["Scan"].unique()

    Base_pros = Pat_df.loc[Pat_df["Mask"] == "shrunk_pros"]["Median"].values[0]
    Base_psoas = Pat_df.loc[Pat_df["Mask"] == "psoas"]["Median"].values[0]

    for Scan in Scans:

    
        ImageFile = PatID + "_" + Scan + "_Raw.nii"

        Val_pros = Pat_df.loc[(Pat_df["Mask"] == "shrunk_pros") & (Pat_df["Scan"] == Scan)]["Median"].values[0]
        Val_psoas = Pat_df.loc[(Pat_df["Mask"] == "psoas") & (Pat_df["Scan"] == Scan)]["Median"].values[0]

        factor_pros = Base_pros / Val_pros
        factor_psoas = Base_psoas / Val_psoas

        pat_path = os.path.join(nifti_dir, t_dir, PatID, Scan)
        
        IF.RescaleImage(pat_path, factor_pros, PatID, Scan, "Pros")
        IF.RescaleImage(pat_path, factor_psoas, PatID, Scan, "Psoas")

