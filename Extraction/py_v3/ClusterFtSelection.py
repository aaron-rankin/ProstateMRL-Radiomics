from asyncio.windows_events import NULL
import pandas as pd
import numpy as np
from tqdm import tqdm
import UsefulFunctions as UF

Norms = UF.NormArray()
patIDs = UF.SABRPats()

csv_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\Labels\\"
out_dir =  "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\SelectedFts2\\"

# specify t val as may experiment in future
t_vals = np.arange(1, 2.5,0.25)
#cluster_method = "weighted"
cluster_method = "ward"

for t_val in t_vals:

    for n in tqdm(Norms):

        for pat in patIDs:
            # read in feature vals and associated cluster labels
            df_pat = pd.read_csv(csv_dir + pat + "_" + n + "_t" + str(t_val) + "_" + cluster_method + ".csv")

            cluster_num = df_pat["Cluster"].max()
            fts_selected = []
            df_result = pd.DataFrame()

            # for each patient loop through each cluster to get 'best' feature
            for c in range(1, cluster_num):
                df_cluster = df_pat[df_pat["Cluster"] == c]

                # function loops through each cluster and gets feature values
                # performs cross-correlation and returns feature with highest mean correlation to all other features
                # returns NULL if < 3 features in cluster 
                ft_selected = UF.ClusterFtSelection2(df_cluster)

                if ft_selected != NULL:
                    for f in ft_selected:
                        fts_selected.append(f)
            
            # filter through all feature values and select only new features
            
                row = {}
            #print("Pat: {} FTs: {}".format(pat, fts_selected))

            for f in fts_selected:
                row["patID"] = pat
                row["Ft"] = f
                df_result = df_result.append(row, ignore_index=True)
            
            df_result.to_csv(out_dir + pat + "_" + n + "_t" + str(t_val) + "_" + cluster_method +".csv")






