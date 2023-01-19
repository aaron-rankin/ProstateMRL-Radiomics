from asyncio.windows_events import NULL
import pandas as pd
import numpy as np
from tqdm import tqdm
import UsefulFunctions as UF
import matplotlib.pyplot as plt
import seaborn as sns

Norms = UF.NormArray()
patIDs = UF.SABRPats()

csv_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\Labels\\"
out_dir =  "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\RatioPlots\\"

t_val = "2"
cluster_method = "weighted"

for n in tqdm(Norms):
    temp_pat = patIDs[0]
    df_temp = pd.read_csv(csv_dir + temp_pat + "_" + n + "_t" + str(t_val) + "_" + cluster_method + ".csv")
    df_temp = df_temp[["PatID", "FeatureName", "Cluster"]]
    df_temp = df_temp.drop_duplicates()
    fts = df_temp["FeatureName"].unique()

    df_result = pd.DataFrame()
    for f in fts:
        linked_fts_1 = UF.ClusterLinkedFts(f, df_temp)
        for pat in patIDs:
            df_pat = pd.read_csv(csv_dir + pat + "_" + n + "_t" + str(t_val) + "_" + cluster_method + ".csv")
            df_pat = df_pat[["PatID", "FeatureName", "Cluster"]]
            df_pat = df_pat.drop_duplicates()

            linked_fts_2 = UF.ClusterLinkedFts(f, df_pat)
            row = {}
            sim_fts, r1, r2, r3 = UF.ClusterSimilarity(linked_fts_1, linked_fts_2)
            row["PatID"], row["Feature"] = pat, f
            row["Num_Sim_Fts"], row["Ratio"] = sim_fts, r3
            df_result = df_result.append(row, ignore_index=True)

    df_matrix = df_result[["Feature", "PatID", "Ratio"]]

    df_matrix = df_matrix.pivot(index="Feature", columns="PatID")

    plt.figure(figsize=(20,20))
    sns.set_theme(style = "white")
    plt.title("Cluster Similarity - {} ({} - t = {})".format(n, cluster_method, str(t_val)), fontsize = 40)
    #sns.diverging_palette(150, 275, s=80, l=55, as_cmap=True)
    sns.color_palette("vlag", as_cmap=True)
    sns.heatmap(df_matrix, vmin=-1, vmax=1, cmap="vlag")
    plt.savefig(out_dir + n + "_t" + str(t_val) + "_" + cluster_method + ".png")
    #plt.show()   