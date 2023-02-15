import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import PlottingFunctions as PF
root = UF.DataRoot(2)

dir = (root + "Aaron\ProstateMRL\Data\Paper1\Longitudinal\Clustering\\Labels\\")

csvs = os.listdir(dir)
fts = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\Longitudinal\Clustering\\HM_SelectedFeatures.csv")
fts_s = fts["Feature"].values

# strip the original_ from the feature names
fts_s = [x.replace("original_", "") for x in fts_s]


colours = {"N": "grey", "Y": "red"}

print(fts_s)

# remove any csvs that do not have HM in the name
csvs = [x for x in csvs if "HM" in x]


for x in csvs[0:1]:
   df = pd.read_csv(dir + x)
   df = df[['Feature', 'Cluster', 'Fraction', 'FeatureChange']]
   df['Feature'] = df['Feature'].str.replace('original_', '')
   df["Selected"] = "N"
   for f in fts_s:
      df.loc[df["Feature"] == f, "Selected"] = "Y"
   
   #print features that are selected   
   print(df.loc[df["Selected"] == "Y", "Feature"].unique())
   df.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\Longitudinal\Clustering\\" + x, index=False)
   clusters = df["Cluster"].unique()
   for c in clusters[0:3]:
      df_c = df[df["Cluster"] == c]
      df_c = df_c.sort_values("Fraction")
      plt.figure(figsize=(10, 5))

      print(df_c.head())
      fts = df_c["Feature"].unique()
      
      plt.figure(figsize=(10, 5))
      sns.set_theme(style="darkgrid")
      #sns.set_context("paper", font_scale=1.5)
      sns.set_style("ticks")
      for ft in fts:
         df_ft = df_c.loc[df_c["Feature"] == ft]
      #sns.lineplot(df_c["Fraction"], df_c["FeatureChange"], hue=df_c["Selected"], palette=colours)
         if ft in fts_s:                  
            sns.set_theme(style="darkgrid")

            sns.lineplot(data = df_ft, x = "Fraction", y ="FeatureChange", hue="Selected", palette=colours,legend=False)
      
         else:
            sns.set_theme(style="darkgrid")

            sns.lineplot(data = df_ft, x = "Fraction", y ="FeatureChange", hue="Selected", palette=colours, alpha=0.5, legend=False)

            #sns.lineplot(df_ft["Fraction"], df_ft["FeatureChange"], c="b")
            #sns.lineplot(df_ft["Fraction"], df_ft["FeatureChange"], marker="o", c="b")
      plt.title("Cluster " + str(c))
      plt.xticks(np.arange(1,5.1,1))
      plt.xlabel("Fraction")
      plt.ylabel("Feature Change")
      plt.legend(title = "Feature Selected")
      new_labels = ['No', 'Yes']
      #for t, l in zip(plt.legend().texts, new_labels): t.set_text(l) 


      #plt.show()
   # plot the median signal intensity for each patient using seaborn facetgrid
   #g = sns.FacetGrid(df, col="Cluster", col_wrap=5, height=2, aspect=1.5)
   # g.map(plt.plot, "Fraction", "FeatureChange", marker="o", c="Selected" )
   # g.set_axis_labels("Fraction", "Median Signal Intensity")
   # g.set_titles("{col_name}")
   # plt.show() 


