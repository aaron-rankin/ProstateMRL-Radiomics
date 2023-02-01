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
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Features\delta_fts_pVol.csv")
fractions = df_all["Fraction"].unique()
fts = df_all["Feature"].unique()

df_res = pd.DataFrame()

matrix = np.zeros((len(fts), len(fts)))

# loop through all features
df_fr1 = df_all[df_all["Fraction"].isin([4,5])]

for i, ft1 in enumerate(fts):
    vals_ft1 = df_fr1[df_fr1["Feature"] == ft1]["FeatureValue"].values
    for j, ft2 in enumerate(fts):
        vals_ft2 = df_fr1[df_fr1["Feature"] == ft2]["FeatureValue"].values
        rho = stats.spearmanr(vals_ft1, vals_ft2)[0]
        matrix[i,j] = rho

df_res = pd.DataFrame(matrix, index=fts, columns=fts)
#print(df_res)

df_res.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Delta\CorrMatrix.csv")

# plot heatmap
plt.figure(figsize=(20,20))
sns.heatmap(df_res, cmap="RdBu_r", vmin=-1, vmax=1, square=True)
plt.savefig(root + "Aaron\ProstateMRL\Data\Paper1\Delta\CorrMatrix.png")
plt.clf()

# show only values less than or equal to 0.5
df_res = abs(df_res)
df_res[df_res >= 0.5] = 0
df_res.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Delta\CorrMatrix_masked.csv")
plt.figure(figsize=(20,20))
sns.heatmap(df_res, cmap="RdBu_r", vmin=0, vmax=0.5, square=True)
plt.savefig(root + "Aaron\ProstateMRL\Data\Paper1\Delta\CorrMatrix_masked.png")