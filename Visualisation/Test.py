import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import PlottingFunctions as PF
root = UF.DataRoot(2)


def SignalPlotPP(df, pat, fts, title, savepath, col_wrap_num, wrap_by):
   '''
   Given a df, patient and selected ft array, plots the signal for the given features
   Per Patient
   '''
   
   df_pat = df[df['PatID'] == pat]
   df_pat = df_pat[df_pat['Feature'].isin(fts)]
   print(df_pat.head())
   df_pat["Fraction"] = df_pat["Fraction"].astype(int)
   fractions = df_pat["Fraction"].unique()

   fig = plt.figure(figsize=(20, 10))
   g = sns.FacetGrid(df_pat, col="Feature", col_wrap=col_wrap_num, aspect=1.5)
   g.fig.subplots_adjust(top=0.9)
   g.fig.suptitle("{} - {}".format(title, str(pat)))
   g.map(sns.scatterplot, x=df_pat["Fraction"], y=df_pat["FeatureChange"], hue=df_pat["Feature"])
   g.map(sns.lineplot, x=df_pat["Fraction"], y=df_pat["FeatureChange"],hue=df_pat["Feature"])
   g.set_axis_labels("Fraction", "Feature Change")
   g.set_titles("{col_name}")

   plt.savefig(savepath + "{}_{}.png".format(title, str(pat)))
   plt.clf()

def SignalPlotPP(df, pat, fts, title, savepath, col_wrap_num, wrap_by):
   '''
   Given a df, patient and selected ft array, plots the signal for the given features
   Per Patient
   '''
   
   df_pat = df[df['PatID'] == pat]
   df_pat = df_pat[df_pat['Feature'].isin(fts)]
   print(df_pat.head())
   df_pat["Fraction"] = df_pat["Fraction"].astype(int)
   fractions = df_pat["Fraction"].unique()

   plt.figure(figsize=(20, 10))
   g = sns.FacetGrid(df_pat, col="Feature", col_wrap=col_wrap_num, aspect=1.5)
   g.fig.subplots_adjust(top=0.9)
   g.fig.suptitle("{} - {}".format(title, str(pat)))
   g.map(sns.scatterplot, x=df_pat["Fraction"], y=df_pat["FeatureChange"], hue=df_pat["Feature"])
   g.map(sns.lineplot, x=df_pat["Fraction"], y=df_pat["FeatureChange"],hue=df_pat["Feature"])
   g.set_axis_labels("Fraction", "Feature Change")
   g.set_titles("{col_name}")

   plt.savefig(savepath + "{}_{}.png".format(title, str(pat)))
   plt.clf()



df_ft = pd.read_csv(root + "\Aaron\ProstateMRL\Data\Paper1\Longitudinal\Clustering\SelectedFeatures.csv")
df_vals = pd.read_csv(root + "\Aaron\ProstateMRL\Data\Paper1\Features\All_fts_change.csv")

fts = df_ft['Feature'].unique()
PatIDs = df_vals['PatID'].unique()

savepath = root + "\Aaron\ProstateMRL\Data\Paper1\Plots\Signal\\"


print(fts)


for pat in PatIDs:
    SignalPlotPP(df_vals, pat, fts, "Cluster Features", savepath, 5, "Feature")
