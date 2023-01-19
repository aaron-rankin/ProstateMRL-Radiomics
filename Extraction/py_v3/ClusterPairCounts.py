import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import UsefulFunctions as UF
import numpy as np

labels_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\Labels\\"
out_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\PairCounts\\"
 

Norms = UF.NormArray()
patIDs = UF.SABRPats()

t_vals = np.arange(1, 2.5,0.25)
cluster_method = "weighted"
#cluster_method = "ward"

for t_val in t_vals:

    for n in tqdm(Norms):
        df_all = pd.DataFrame()
        df_temp = pd.read_csv(labels_dir + patIDs[0] + "_" + n + "_t2_ward.csv")

        fts = df_temp.FeatureName.unique()
            
        matrix = np.zeros((len(fts),len(fts)))
        
        for pat in patIDs:
            df_pat = pd.read_csv(labels_dir + pat + "_" + n + "_t" + str(t_val) + "_" + cluster_method + ".csv")
            df_pat = df_pat[["PatID", "FeatureName", "Cluster"]]
            df_pat = df_pat.drop_duplicates()
            
            for i in range(len(fts)):
                for j in range(len(fts)):
                    ft1 = fts[i]
                    ft2 = fts[j]

                    ft1_c = df_pat[df_pat["FeatureName"] == ft1]["Cluster"].values[0]
                    ft2_c = df_pat[df_pat["FeatureName"] == ft2]["Cluster"].values[0]

                    if ft1_c == ft2_c:
                        matrix[i,j] = matrix[i,j] + 1
                    else:
                        matrix[i,j] = matrix[i,j]

            df_matrix = pd.DataFrame(matrix, columns=fts, index=fts)

        plt.figure(figsize=(20,20))
        sns.set_theme(style = "white")
        plt.title("Clustered ft pairs - {} ({} - t = {})".format(n, cluster_method, str(t_val)), fontsize = 40)
        sns.heatmap(df_matrix, cmap='viridis', cbar_kws={'label': 'Pair counts'})
        plt.savefig(out_dir + n + "_t" + str(t_val) + "_" + cluster_method + ".png")
    

