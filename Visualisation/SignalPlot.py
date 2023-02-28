import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
root = UF.DataRoot(2)

df_fts = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Raw\\Features\\Longitudinal_All_fts.csv")
#print(df_fts.head())


# filter for only original_firstorder_median
df_fts = df_fts[df_fts["Feature"] == "original_firstorder_Median"]
PatIDs = df_fts["PatID"].unique()

# plot the median signal intensity for each patient using seaborn facetgrid
g = sns.FacetGrid(df_fts, col="PatID", col_wrap=5, height=2, aspect=1.5)
g.map(plt.plot, "Fraction", "FeatureValue", marker="o")
g.set_axis_labels("Fraction", "Signal", fontsize=16)
# change fontsize of x and y labels
# change fontsize of x and y ticks
plt.tick_params(labelsize=16)
# set title of total figure
g.fig.suptitle("Median Prostate Signal Intensity", fontsize=30, y=1.0)
g.figure.subplots_adjust(top=0.9)
g.set_titles("{col_name}")
plt.show()
