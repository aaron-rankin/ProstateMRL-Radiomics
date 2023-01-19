import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import sklearn.metrics as metrics
import sklearn.cluster as sc
from scipy.cluster.hierarchy import dendrogram
import UsefulFunctions as UF
from matplotlib.colors import LinearSegmentedColormap

Norms = UF.NormArray()
patIDs = UF.SABRPats()
cluster_type = "AffinityPropagation"

for n in tqdm(Norms):
    # csv containing all ft vals for each patient per norm
    ft_vals = ft_vals = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\VolIndFts\\" + n + ".csv")
    ft_vals["PatID"] = ft_vals["PatID"].astype(str)
    
    # create empty dataframe to house features and cluster for each patient
    df_hm = pd.DataFrame()
    cluster_max = 0

    for pat in patIDs:
        # get patient cluster labels
        ft_labels = pd.read_csv("D:\data\Aaron\ProstateMRL\Data\MRLPacks\\Clustering\\" + cluster_type + "\\Labels\\" + pat + "_" + n + "_ClusterLabel.csv")
        ft_labels.set_index("FeatureName", inplace=True)
        
        # get patient values
        ft_vals_p = ft_vals[ft_vals["PatID"] == pat]
        ft_vals_p = ft_vals_p.merge(ft_labels, left_on="FeatureName", right_on="FeatureName")

        ft_vals_p = ft_vals_p[["PatID", "Cluster", "FeatureName"]]
        # only need one timepoint for each feature to get cluster
        ft_vals_p.drop_duplicates(inplace=True)
        clusters = ft_vals_p["Cluster"].unique()
        cluster_num = len(clusters)
        if cluster_num > cluster_max:
            cluster_max = cluster_num

        ft_vals_p = ft_vals_p.pivot(index="FeatureName", columns="PatID", values="Cluster")
        # merge to get heatmap over all patients per norm
        df_hm = df_hm.merge(ft_vals_p, left_index=True, right_index=True, how="outer")
        print("{} - {} - {}".format(n, pat, cluster_num))
        

    
    # plot
    cmap = plt.get_cmap('viridis', cluster_max)#, 4)

    plt.figure(figsize=(20,25))
    g = sns.heatmap(df_hm, cmap=cmap, cbar=True, yticklabels=True, xticklabels=True)
    colorbar = g.collections[0].colorbar
    plt.title("Clustered Features - {}".format(n), fontsize=30)
    plt.yticks(fontsize = 8)
    plt.xlabel("PatID", fontsize=20)
    plt.ylabel("FeatureName", fontsize=20)
    colorbar.set_ticks(np.arange(0, cluster_max, 1))
    colorbar.set_ticklabels(np.arange(0, cluster_max, 1), )
    colorbar.set_label("Cluster", fontsize=20)
    plt.savefig("D:\data\Aaron\ProstateMRL\Data\MRLPacks\\Clustering\\" + cluster_type + "\\TilePlots\\" + n + "_ClusterTile.png")
