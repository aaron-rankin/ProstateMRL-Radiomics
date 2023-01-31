import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import UsefulFunctions as UF

Norms = UF.NormArray()
patIDs = UF.SABRPats()

vals_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\Labels\\"
out_dir = "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\SignalPlots\\"
#cluster_type = "AffinityPropagation"
cluster_method = "ward"
t_val = "2"

t_vals = np.arange(1, 2.5, 0.25)

for t_val in t_vals: 
    for n in tqdm(Norms):
        # csv containing all ft vals for each patient per norm
    
        for pat in patIDs:
            df_pat = pd.read_csv(vals_dir + pat + "_" + n + "_t" + str(t_val) + "_" + cluster_method + ".csv")
            fig = plt.figure(figsize=(10, 7))
            g = sns.FacetGrid(df_pat, col = "Cluster", col_wrap=4)
            g.tight_layout()
            g.fig.suptitle("{} {} - {}  - t_val = {} Clusters".format(pat, n, cluster_method, str(t_val), fontsize=40))
            g.map_dataframe(sns.scatterplot, x="DaysDiff", y="FeatureChange", hue="FeatureName")
            g.map_dataframe(sns.lineplot, x="DaysDiff", y="FeatureChange", hue="FeatureName")
            g.savefig(out_dir + pat + "_" + n + "_t" + str(t_val) + "_" + cluster_method + "_SignalClusters.png")
            plt.clf()
