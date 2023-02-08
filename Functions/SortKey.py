import pandas as pd
import numpy as np
import datetime

import sys
import os

current = os.path.dirname(os.path.realpath("Test.ipynb"))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(2)

# Patient Key

All_url = root + "Aaron\\ProstateMRL\\Code\\PatKeys\\AllPatientKey.csv"
AllKey = pd.read_csv(All_url)
L_url = root + "Aaron\\ProstateMRL\\Code\\PatKeys\\LimbusKey.csv"
LimbusKey = pd.read_csv(L_url)

# filter through treatment
ts = AllKey.Treatment.unique()
print(AllKey)
new_key = pd.DataFrame()

# loop through ts
for t in ts:
    t_key = AllKey[AllKey["Treatment"] == t]
    t_patIDs = t_key["PatID"].unique().astype(str)

    # loop through all patients
    for pat in t_patIDs:
        p_key = t_key[t_key["PatID"].isin([pat])]

        # Strip MR string from column and sort
        p_key["Scan"] = p_key["Scan"].str.replace("MR", "")
        p_key["Scan"] = p_key["Scan"].astype(int)
        p_key = p_key.sort_values(by=["Scan"])
        # add MR back to column
        p_key["Scan"] = p_key["Scan"].astype(str)
        p_key["Scan"] = "MR" + p_key["Scan"]

        
        # Get first date
        first_date = UF.FixDate(p_key.iloc[0]["Date"])
        p_key["Days"] = p_key["Date"].apply(lambda x: (UF.FixDate(x) - first_date).days)
        p_key["Fraction"] = p_key.reset_index().index + 1

        new_key = new_key.append(p_key)
    
new_key.to_csv(root + "Aaron\\ProstateMRL\\Code\\PatKeys\\LimbusKey_s.csv", index=False)

# find overlap between keys
new_key = new_key[new_key["PatID"].isin(LimbusKey["PatID"])]
new_key.to_csv(root + "Aaron\\ProstateMRL\\Code\\PatKeys\\LimbusKey_s.csv", index=False)


