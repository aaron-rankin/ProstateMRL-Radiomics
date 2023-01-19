import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.spatial import distance
from tqdm import tqdm
import UsefulFunctions as UF

root = 'D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\VolIndFts\\'

# csvs for each normalisation arm
Norms = UF.NormArray()
patIDs = UF.SABRPats()

for n in tqdm(Norms):
    df_allvals = pd.read_csv(root + n + ".csv")
    
    df_allvals.PatID = df_allvals.PatID.astype(str)

    # create a dict with dfs for each patient
    dict_patvals = {elem : pd.DataFrame for elem in patIDs}
    for key in dict_patvals.keys():
        dict_patvals[key] = df_allvals[:][df_allvals.PatID == key]

    # loop through each patient
    for pat in dict_patvals.keys():
        df_pat = dict_patvals[pat]
        fts = df_pat.FeatureName.unique()

        # get an nxn matrix to fill
        matrix_dist = np.zeros((len(fts),len(fts)))

        # loop through fts
        for i in range(len(fts)):
            for j in range(len(fts)):
                # calc euclidian distance between 2 ft values arrays
                ft_1 = df_pat[df_pat.FeatureName == fts[i]].FeatureChange # FeatureValue
                ft_2 = df_pat[df_pat.FeatureName == fts[j]].FeatureChange # FeatureValue
                # returns distance to matrix
                matrix_dist[i,j] = distance.euclidean(ft_1, ft_2)
        
        # output to csv full matrix
        df_dist = pd.DataFrame(matrix_dist, columns = fts, index = fts)
        df_dist.to_csv('D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DistanceMatrices\\csvs\\{}.csv'.format(pat + "_" + n + "_DM"))
        
        # plot a heatmap using matrix
        plt.figure(figsize=(20,20))
        sns.set_theme(style = "white")
        plt.title("DM {} {}".format(pat, n), fontsize = 40)
        sns.heatmap(df_dist, cmap='viridis', cbar_kws={'label': 'Euclidean Distance'})
        plt.savefig('D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DistanceMatrices\\figs\\{}.png'.format(pat + "_" + n + "_DM"))