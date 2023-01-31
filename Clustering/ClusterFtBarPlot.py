import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster
import os
from tqdm import tqdm
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(2)
patIDs = UF.SABRPats()
csv_dir =  root + "Aaron\\ProstateMRL\\Data\\Paper1\\Clustering\\SelectedFeatures\\csvs\\"
barp_dir = root + "Aaron\\ProstateMRL\\Data\\Paper1\\Clustering\\SelectedFeatures\\BarPlots\\"

Norms = UF.NormArray()[0:1]
patIDs = UF.SABRPats()
#t_vals = np.arange(1,2.5,0.25)
t_vals = [2]
cluster_method = "weighted"
#cluster_method = "ward"

groups = ["firstorder", "glcm", "glszm", "glrlm", "ngtdm", "gldm"]
df_all = pd.DataFrame()
for p in patIDs:
    df_pat = pd.read_csv(csv_dir + p + ".csv")

    df_all = df_all.append(df_pat)

df_counts = df_all.Ft.value_counts().rename_axis("Ft").reset_index(name="Counts")
df_counts["FtGroup"] = df_counts["Ft"].str.split("_")
df_counts["FtGroup"] = df_counts["FtGroup"].str[1]

df_plot = df_counts[df_counts["Counts"] > 4]

plt.figure(figsize=(20,20))
sns.set_theme(style = "darkgrid")
plt.title("Selected Features", fontsize=40)
sns.barplot(data=df_plot, x="Counts", y="Ft", hue="FtGroup", dodge=False, palette="deep")
plt.xlabel("Number of patients that selected feature", labelpad = 14, fontsize = 20)
plt.xlim((0,20))
plt.xticks(np.arange(0,21,2))
plt.ylabel("Selected feature", labelpad = 14)
plt.legend(title = "", loc='lower right', borderaxespad=0, fontsize = 20)
plt.savefig(barp_dir + "Overall.png")
plt.clf()

#df_plot.to_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\FinalFt\\" + n + "_SelectedFts.csv")

