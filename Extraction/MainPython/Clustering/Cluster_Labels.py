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

DM_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\DM\\csvs\\"
out_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\Clustering\\"

# t val specifies threshold used for hierarchical clustering distance - needs a sensitivity test
t_val = 2
cluster_method = "weighted"
#cluster_method = "ward"

for pat in patIDs:
    # read in DM
    df_DM = pd.read_csv(DM_dir + pat + ".csv")
    df_DM.set_index("Unnamed: 0", inplace=True)
    arr_DM = df_DM.to_numpy()
    fts = df_DM.columns

    # create temp df to hold ft name and label
    df_labels = pd.DataFrame()
    df_labels["FeatureName"] = fts

    # cluster function using DM, need to experiment with t_val and method
    df_labels["Cluster"] = spch.fclusterdata(arr_DM, t=t_val, criterion="distance", method=cluster_method)
    df_labels.set_index("FeatureName", inplace=True)
    
    # read in df with ft vals and merge
    ft_vals = pd.read_csv(root +"Aaron\\ProstateMRL\\Data\\Paper1\\Features\\All_fts_pVol.csv")
    ft_vals["PatID"] = ft_vals["PatID"].astype(str)
    pat_ft_vals = ft_vals[ft_vals["PatID"] == pat]
    pat_ft_vals = pat_ft_vals.merge(df_labels, left_on="Feature", right_on="FeatureName")

    # output is feature values w/ cluster labels
    pat_ft_vals.to_csv(out_dir + "Labels\\" + pat + ".csv")
