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

key_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\PatientKey_sorted.csv")
treatments = key_df.Treatment.unique()

# Inter-fraction signal changes
sig_url = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges_v2\\"
sig_changes = os.listdir(sig_url)

sig_all_df = pd.DataFrame()

for i in sig_changes:
    pat_df = pd.read_csv((sig_url + i))
    sig_all_df = sig_all_df.append(pat_df)

sig_all_df.to_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Combined_csvs\\Signal_changes.csv")