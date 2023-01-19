import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster
import UsefulFunctions as UF
from tqdm import tqdm

csv_dir =  "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\SelectedFts2\\"
barp_dir =  "D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\BarPlots\\"

Norms = UF.NormArray()[0:1]
patIDs = UF.SABRPats()
#t_vals = np.arange(1,2.5,0.25)
t_vals = [2]
cluster_method = "weighted"
#cluster_method = "ward"

groups = ["firstorder", "glcm", "glszm", "glrlm", "ngtdm", "gldm"]
for t_val in t_vals:

    for n in tqdm(Norms):
        
        df_all = pd.DataFrame()
        for p in patIDs:
            df_pat = pd.read_csv(csv_dir + p + "_" + n + "_t" + str(t_val) + "_" + cluster_method + ".csv")# + t_val + "_FinalFts.csv")

            df_all = df_all.append(df_pat)

        df_counts = df_all.Ft.value_counts().rename_axis("Ft").reset_index(name="Counts")
        df_counts["FtGroup"] = df_counts["Ft"].str.split("_")
        df_counts["FtGroup"] = df_counts["FtGroup"].str[0]

        df_plot = df_counts[df_counts["Counts"] > 4]
        
        # rgb_vals = sns.color_palette("deep", len(groups))
        # colourmap = dict(zip(groups, rgb_vals))

        # plt.figure(figsize=(20,20))
        # sns.set_theme(style = "darkgrid")
        # plt.title("Selected Features - {} ({}, t = {})".format(n, cluster_method, str(t_val)), fontsize=40)
        # sns.barplot(data=df_plot, x="Counts", y="Ft", hue="FtGroup", dodge=False, palette=colourmap)
        # plt.xlabel("Number of patients that selected feature", labelpad = 14, fontsize = 20)
        # plt.xlim((0,20))
        # plt.xticks(np.arange(0,21,2))
        # plt.ylabel("Selected feature", labelpad = 14)
        # plt.legend(title = "", loc='lower right', borderaxespad=0, fontsize = 20)
        # #plt.savefig(barp_dir + n + "_t" +str(t_val) + "_" + cluster_method + ".png")
        # plt.clf()

        df_plot.to_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\FinalFt\\" + n + "_SelectedFts.csv")

