import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# read csv file
delta_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DeltaTrial\\Delta_fts_selected.csv")
ft_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\VolIndFts\\Raw.csv")
# plot feature values over time
#patIDs = df["PatID"].unique().astype(str)
#print(patIDs)
# loop through all patients

fts = delta_df["FeatureName"].unique()

# loop through all features
#for j in range(len(fts)):
# select feature
df_ft = ft_df[ft_df["FeatureName"].isin(fts)]
print(df_ft.shape)
# plot feature values over time
plt.figure(figsize=(10, 10))
g = sns.FacetGrid(df_ft, col="FeatureName", col_wrap=4)
g.tight_layout()
cl = sns.color_palette("hls", 20)
g.map_dataframe(sns.scatterplot,x="DaysDiff", y="FeatureChange", hue="PatID", )
g.map_dataframe(sns.lineplot,x="DaysDiff", y="FeatureChange", hue="PatID", legend=False)
g.savefig("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\DeltaTrial\\DeltaSignal\\" + "test.png")
plt.clf()