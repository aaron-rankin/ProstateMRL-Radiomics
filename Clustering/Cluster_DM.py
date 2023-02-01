import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd
import pingouin as pg
from scipy import stats
from tqdm import tqdm
import sys
from scipy.spatial import distance

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(2)

# read in fts from csv
df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Features\All_fts_pVol.csv")

patIDs = df_all["PatID"].unique()
fts = df_all["Feature"].unique()
# loop through patients
for pat in tqdm(patIDs):
    df_pat = df_all[df_all["PatID"] == pat]

    # empty matrix
    mat = np.zeros((len(fts), len(fts)))

    for ft1 in range(len(fts)):
        vals_ft1 = df_pat[df_pat["Feature"] == fts[ft1]]["FeatureChange"].values

        for ft2 in range(len(fts)):
            vals_ft2 = df_pat[df_pat["Feature"] == fts[ft2]]["FeatureChange"].values

            # calculate correlation
            mat[ft1, ft2] = distance.euclidean(vals_ft1, vals_ft2)
    
    # save matrix
    df_dist = pd.DataFrame(mat, columns = fts, index = fts)
    df_dist.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Longitudinal\\DM\\csvs\\" + str(pat) + ".csv")

    # plot matrix
    plt.figure(figsize=(20,20))
    sns.set_theme(style="white")
    plt.title("DM - {}".format(pat), fontsize=40)
    sns.heatmap(df_dist, cmap='viridis', cbar_kws={'label': 'Euclidean Distance'})
    plt.savefig(root + '\\Aaron\\ProstateMRL\\Data\\Paper1\\Longitudinal\\DM\\Figs\\' + str(pat) + '.png')
