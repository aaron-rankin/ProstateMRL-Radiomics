import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
from scipy.cluster.hierarchy import dendrogram
import UsefulFunctions as UF
import scipy.cluster.hierarchy as spch

Norms = UF.NormArray()
patIDs = UF.SABRPats()

DM_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DistanceMatrices\\csvs\\"
out_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\"

# t val specifies threshold used for hierarchical clustering distance - needs a sensitivity test
t_vals = np.arange(1, 2.5, 0.25)
#cluster_method = "weighted"
cluster_method = "ward"

for t_val in t_vals:
    for n in tqdm(Norms):

        for pat in patIDs:
            # read in DM
            df_DM = pd.read_csv(DM_dir + pat + "_" + n + "_DM.csv")
            df_DM = df_DM.drop(columns=['Unnamed: 0'])

            arr_DM = df_DM.to_numpy()
            fts = df_DM.columns

            # create temp df to hold ft name and label
            df_labels = pd.DataFrame()
            df_labels["FeatureName"] = fts

            # cluster function using DM, need to experiment with t_val and method
            df_labels["Cluster"] = spch.fclusterdata(arr_DM, t=t_val, criterion="distance", method=cluster_method)
            df_labels.set_index("FeatureName", inplace=True)
            
            # read in df with ft vals and merge
            ft_vals = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\VolIndFts\\" + n + ".csv")
            ft_vals["PatID"] = ft_vals["PatID"].astype(str)
            pat_ft_vals = ft_vals[ft_vals["PatID"] == pat]
            pat_ft_vals = pat_ft_vals.merge(df_labels, left_on="FeatureName", right_on="FeatureName")

            # output is feature values w/ cluster labels
            pat_ft_vals.to_csv(out_dir + "Labels\\" + pat + "_" + n + "_t" + str(t_val) + "_" + cluster_method + ".csv")
