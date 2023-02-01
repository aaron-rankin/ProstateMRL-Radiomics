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

labels_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\Longitudinal\\Clustering\\Labels\\"
out_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\Longitudinal\\Clustering\\"
# t val specifies threshold used for hierarchical clustering distance - needs a sensitivity test
t_val = 2
df_result = pd.DataFrame()
for pat in patIDs:
    # read in feature vals and associated cluster labels
    df_pat = pd.read_csv(labels_dir + pat + ".csv")

    cluster_num = df_pat["Cluster"].max()
    fts_selected = []
    df_result_pat = pd.DataFrame()

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

    for f in fts_selected:
        row["patID"] = pat
        row["Feature"] = f
        df_result_pat = df_result_pat.append(row, ignore_index=True)
    
    #df_result_pat.to_csv(out_dir + pat + ".csv")
    df_result = df_result.append(df_result_pat, ignore_index=True)

df_result = df_result.Feature.value_counts().rename_axis("Feature").reset_index(name="Counts")
#df_result["FeatureGroup"] = df_counts["Feature"].str.split("_")
#df_result["FeatureGroup"] = df_counts["FeatureGroup"].str[1]

df_result = df_result[df_result["Counts"] > 4]

# drop counts
df_result.drop(columns=["Counts"], inplace=True)
df_result.to_csv(out_dir + "SelectedFeatures.csv")





