import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pingouin as pg
from scipy import stats
from tqdm import tqdm
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(2)

# read in fts from csv
df_corr = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Delta\CorrMatrix.csv")

fts = df_corr["Unnamed: 0"].values

array_corr = df_corr.values[:,1:]
array_corr = abs(array_corr)

results = np.zeros((len(fts), len(fts)))
selected_fts = []

for i in range(len(fts)):
    for j in range(len(fts)):
        
        if array_corr[i,j] <= 0.5:
            results[i,j] = array_corr[i,j]
            selected_fts.append([fts[i], fts[j]])
        else:
            results[i,j] = 1

df_res = pd.DataFrame(results, columns=fts, index=fts)
plt.figure(figsize=(20,20))
sns.heatmap(df_res, cmap="RdBu_r", vmin=0, vmax=0.5, square=False)
# plt.show()

# loop through results with ft pairs and select ft with lowest mean value
# create an empty array to store the results
fts_keep = []
fts_remove = []
for i in range(len(selected_fts)):
    # select ft pair
    df_ft1 = df_corr[df_corr["Unnamed: 0"] == selected_fts[i][0]]
    df_ft2 = df_corr[df_corr["Unnamed: 0"] == selected_fts[i][1]]
    # get mean values across row
    mean_ft1 = float(df_ft1.mean(axis=1))
    mean_ft2 = float(df_ft2.mean(axis=1))

    # compare mean values
    if mean_ft1 < mean_ft2:
        fts_keep.append(selected_fts[i][0])
        fts_remove.append(selected_fts[i][1])
    else:
        fts_keep.append(selected_fts[i][1])
        fts_remove.append(selected_fts[i][0])
    
# remove duplicates
fts_keep = list(dict.fromkeys(fts_keep))
fts_remove = list(dict.fromkeys(fts_remove))

# compare lists
fts_keep2 = [x for x in fts_keep if x not in fts_remove]

# print results
print("Features to keep: {}".format(len(fts_keep2)))
print(fts_keep2)

# save results
df_fts = pd.DataFrame(fts_keep2, columns=["Features"])
df_fts.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Delta\\delta_selected_fts.csv", index=False)
