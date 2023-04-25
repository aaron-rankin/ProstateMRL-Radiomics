import os
import numpy as np
import SimpleITK as sitk
import pandas as pd
from tqdm import tqdm
from Functions import UsefulFunctions as UF

def dice_score(mask1_path, mask2_path):
    # Load the masks as SimpleITK images
    mask1 = sitk.ReadImage(mask1_path)
    mask2 = sitk.ReadImage(mask2_path)

    # Convert the masks to numpy arrays
    mask1_arr = sitk.GetArrayFromImage(mask1)
    mask2_arr = sitk.GetArrayFromImage(mask2)

    # make array binary
    mask1_arr[mask1_arr > 0] = 1
    mask2_arr[mask2_arr > 0] = 1

    # Flatten the arrays to 1D
    mask1_flat = mask1_arr.flatten()
    mask2_flat = mask2_arr.flatten()
    
    if len(mask1_flat) > len(mask2_flat):
        mask1_flat = mask1_flat[:len(mask2_flat)]
    elif len(mask1_flat) < len(mask2_flat):
        mask2_flat = mask2_flat[:len(mask1_flat)]

    # Calculate the intersection and union of the masks
    intersection = np.sum(mask1_flat * mask2_flat)
    union = np.sum(mask1_flat) + np.sum(mask2_flat)

    # Calculate the DICE score
    dice = 2 * intersection / union

    return dice

all_key = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Code\\PatKeys\\LimbusKey_s.csv")
all_key = all_key[all_key["Treatment"] == "SABR"]

nifti_dir = "D:\\data\\prostateMR_radiomics\\nifti\\"

# get list of patients
patIDs = all_key["PatID"].unique()
df_res = pd.DataFrame()
for pat in tqdm(patIDs):
    pat_key = all_key[all_key["PatID"] == pat]
    
    t_dir = pat_key["FileDir"].unique()[0]
    pat = UF.FixPatID(pat, t_dir)
    pat_path = nifti_dir + t_dir + "\\" + pat + "\\" 
    scans = pat_key["Scan"].unique()

    for scan in scans:
        mask_dir = pat_path + scan + "\\Masks\\"
        limbus_mask = mask_dir + str(pat) + "_" + scan + "_" + "Limbus_shrunk.nii"
        manual_mask = mask_dir + str(pat) + "_" + scan + "_" + "shrunk_pros.nii"

        if os.path.exists(limbus_mask) and os.path.exists(manual_mask):
            dice = dice_score(limbus_mask, manual_mask)
            df_temp = pd.DataFrame({"PatID": [pat], "Scan": [scan], "Dice": [dice]})
            df_res = df_res.append(df_temp, ignore_index = False)

df_res.to_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\Paper1\\Masks\\DiceScore.csv")