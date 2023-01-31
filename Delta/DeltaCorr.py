import numpy as np
import pandas as pd
import UsefulFunctions as UF
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

dir_in = 'D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DeltaTrial\\DeltaVals\\'
dir_out = 'D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DeltaTrial\\DeltaCorr\\'

Norms = UF.NormArray()[0:1]
patIDs = UF.SABRPats()

for n in Norms:
    df_n = pd.read_csv(dir_in + n + ".csv")

    df_n["PatID"] = df_n["PatID"].astype(str)

    fts = df_n["FeatureName"].unique()
    matrix = np.zeros((len(fts), len(fts)))
    for i in range(len(fts)):
        #print(fts[i])
        fts_1 = df_n[df_n["FeatureName"] == fts[i]].FeatureChange

        for j in range(len(fts)):
            fts_2 = df_n[df_n["FeatureName"] == fts[j]].FeatureChange

            sp = stats.spearmanr(fts_1, fts_2, axis =1).correlation
            matrix[i,j] = abs(sp)


    # for i in range(len(fts)):

    #     for j in range(len(fts)):
    #         corr_val = matrix[i,j] 

    #         if corr_val >= 0.8:
    #             matrix[i,j] = np.nan

    
                
    df_matrix = pd.DataFrame(matrix, columns=fts, index=fts)
    plt.figure(figsize=(20,20))
    sns.set_theme(style = "white")
    #plt.title("DM {} {}".format(pat, n), fontsize = 40)
    sns.heatmap(df_matrix, cmap='viridis', cbar_kws={'label': 'Spearman'})
    plt.savefig(dir_out + n + "_filtered.png")


