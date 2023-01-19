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
import kneed as kd

def plot_dendrogram(cluster, **kwargs):
    # Create linkage matrix and then plot the dendrogram
    #    # create the counts of samples under each node
    counts = np.zeros(cluster.children_.shape[0])
    n_samples = len(cluster.labels_)
    for i, merge in enumerate(cluster.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack(
        [cluster.children_, cluster.distances_, counts]
    ).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

df_key  = pd.read_csv('D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\VolIndFts\\Raw.csv')
df_key.PatID = df_key.PatID.astype(str)
patIDs = df_key['PatID'].unique()
Norms = UF.NormArray()

csv_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DistanceMatrices\\csvs\\"
out_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\"


for n in tqdm(Norms):

    for pat in patIDs:
        # Read in distance matrix for each patient and norm
        df_DM = pd.read_csv(csv_dir + pat + "_" + n + "_DM.csv")
        df_DM = df_DM.drop(columns=['Unnamed: 0'])

        # Cluster
        arr_DM = df_DM.to_numpy()
        # define cluster method - may want to explore other affinity
        for i in range(3,11,1):
            cluster = sc.AgglomerativeClustering(n_clusters=i, affinity='euclidean', linkage='ward')#, distance_threshold=0)
            cluster.fit(arr_DM)
            
            labels = cluster.labels_
            fts = df_DM.columns

            # merge feature names to cluster labels
            df_fts, df_labels = pd.DataFrame(fts, columns=["FeatureName"]), pd.DataFrame(labels, columns=["Cluster"])
            df_out = pd.concat([df_fts, df_labels], axis=1)
            df_out.set_index('FeatureName', inplace=True)
            df_out.to_csv(out_dir + "Labels\\" + pat + "_" + n + "_" + str(i) + "_ClusterLabel.csv")
    