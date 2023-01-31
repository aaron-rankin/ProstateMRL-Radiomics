import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
from scipy.cluster.hierarchy import dendrogram
import scipy.cluster.hierarchy as spch
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(2)
patIDs = UF.SABRPats()

labels_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\Clustering\\Labels\\"
out_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\Clustering\\SelectedFeatures\\"
# t val specifies threshold used for hierarchical clustering distance - needs a sensitivity test
t_val = 2
cluster_method = "weighted"
#cluster_method = "ward"


for pat in patIDs:
    # read in feature vals and associated cluster labels
    df_pat = pd.read_csv(labels_dir + pat + ".csv")

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

        if ft_selected != 0:
            for f in ft_selected:
                fts_selected.append(f)
    
    # filter through all feature values and select only new features
    
        row = {}
    #print("Pat: {} FTs: {}".format(pat, fts_selected))

    for f in fts_selected:
        row["patID"] = pat
        row["Ft"] = f
        df_result = df_result.append(row, ignore_index=True)
    
    df_result.to_csv(out_dir + pat + ".csv")






