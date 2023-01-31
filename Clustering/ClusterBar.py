from cv2 import rotate
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import UsefulFunctions as UF

Norms = UF.NormArray()
patIDs = UF.SABRPats()

cluster_type = "AffinityPropagation"
#cluster_type = "Agglomerative"

all_df = pd.DataFrame()

for n in tqdm(Norms):
    # csv containing all ft vals for each patient per norm
    ft_vals = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\VolIndFts\\" + n + ".csv")
    ft_vals["PatID"] = ft_vals["PatID"].astype(str)
    pat_ft_vals = pd.DataFrame()

    for pat in patIDs:
    #     # get patient values
        pat_ft_vals = ft_vals[ft_vals["PatID"] == pat]

        pat_ft_labels = pd.read_csv("D:\data\Aaron\ProstateMRL\Data\MRLPacks\\Clustering\\" + cluster_type + "\\Labels\\" + pat + "_" + n + "_ClusterLabel.csv")
        pat_ft_labels.set_index('FeatureName', inplace=True)
        # merge
        pat_ft_vals = pat_ft_vals.merge(pat_ft_labels, left_on="FeatureName", right_on="FeatureName")
        clusters = pat_ft_vals["Cluster"].max() + 1
        row = {"Pat": pat, "Normalisation": n, "Clusters": clusters}
        all_df = all_df.append(row, ignore_index=True)


fig = plt.figure(figsize=(10,7))
g = sns.FacetGrid(all_df, col = "Normalisation", col_wrap=4)
g.map_dataframe(sns.barplot, x="Pat", y="Clusters")
for ax in g.axes.flat:
    for label in ax.get_xticklabels():
        label.set_rotation(90)

plt.show()