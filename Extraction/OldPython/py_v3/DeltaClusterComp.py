import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df_cluster = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Clustering\\Agglomerative\\FinalFt\\Raw_SelectedFts.csv")
df_delta = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DeltaTrial\\Delta_fts_selected.csv")
df_vals = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\VolIndFts\\Raw.csv")

fts_cluster = df_cluster.FeatureName.unique()
fts_delta = df_delta.FeatureName.unique()


common = [i for i in fts_cluster if i in fts_delta]
print(common)

plot_delta = df_vals[df_vals["FeatureName"].isin(fts_delta)]
print(plot_delta.shape)
plt.figure(figsize=(10, 10))
sns.set_theme(style="whitegrid")
g = sns.FacetGrid(plot_delta, col="FeatureName", col_wrap=4)
g.set(ylim = (-1.5, 2.5))
g.tight_layout()
cl = sns.color_palette("hls", 20)
g.map_dataframe(sns.scatterplot,x="DaysDiff", y="FeatureChange", hue="PatID", )
g.map_dataframe(sns.lineplot,x="DaysDiff", y="FeatureChange", hue="PatID", legend=False)
g.savefig("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DeltaTrial\\DeltaSignal\\" + "delta.png")
plt.clf()

plot_cluster = df_vals[df_vals["FeatureName"].isin(fts_cluster)]
print(plot_delta.shape)
plt.figure(figsize=(10, 10))
sns.set_theme(style="whitegrid")
g = sns.FacetGrid(plot_cluster, col="FeatureName", col_wrap=4)
g.set(ylim = (-1.5, 2.5))
g.tight_layout()
cl = sns.color_palette("hls", 20)
g.map_dataframe(sns.scatterplot,x="DaysDiff", y="FeatureChange", hue="PatID", )
g.map_dataframe(sns.lineplot,x="DaysDiff", y="FeatureChange", hue="PatID", legend=False)
g.savefig("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DeltaTrial\\DeltaSignal\\" + "cluster.png")
plt.clf()

