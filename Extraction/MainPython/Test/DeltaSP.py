import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy import stats

csv_in  = "C:\\Users\\b01297ar\\Documents\\ProstateMRL-local\\ProstateMRL-Radiomics\\Data\\Delta\\Delta_fts.csv"
patIDs = ['653', '713', '752', '826', '1088', '1089', '1118', '1303', '1307', '1464', '1029', '1302', '1431', '1481', '1540', '1553', '1601', '1642', '829', '955']

# Read csv file
df = pd.read_csv(csv_in)

# loop through all features
fts = df["FeatureName"].unique()

# create an empty array to store the results
results = np.empty((len(fts), len(fts)))

for f1 in fts:
    #select feature
    df_ft = df[df["FeatureName"] == f1]
    fts_1  = df_ft["FeatureChange"].values

    for f2 in fts:
        #select feature
        df_ft = df[df["FeatureName"] == f2]
        fts_2  = df_ft["FeatureChange"].values

        # calculate the correlation between the two features
        corr = stats.spearmanr(fts_1, fts_2)
        results[fts == f1, fts == f2] = abs(corr[0])

# create a dataframe from the results
df_corr = pd.DataFrame(results, index=fts, columns=fts)

# plot the correlation matrix
plt.figure(figsize=(20, 20))
sns.heatmap(df_corr, cmap="YlGnBu")
plt.savefig("C:\\Users\\b01297ar\\Documents\\ProstateMRL-local\\ProstateMRL-Radiomics\\Data\\Delta\\Delta_fts_corr.png")

df_corr.to_csv("C:\\Users\\b01297ar\\Documents\\ProstateMRL-local\\ProstateMRL-Radiomics\\Data\\Delta\\Delta_fts_corr.csv")
