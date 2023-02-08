import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd
import pingouin as pg
from scipy import stats
from tqdm import tqdm
import sys
from scipy.spatial import distance

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF

root = UF.DataRoot(2)

def SignalPlotPP(df, pat, fts, title, savepath, col_wrap_num, wrap_by):
   '''
   Given a df, patient and selected ft array, plots the signal for the given features
   Per Patient
   '''
   
   df_pat = df[df['PatID'] == pat]
   print(df_pat.head())

   fig = plt.figure(figsize=(20, 10))
   g = sns.FacetGrid(df_pat, col=wrap_by, col_wrap=col_wrap_num, aspect=1.5)
   g.fig.subplots_adjust(top=0.9)
   g.fig.suptitle("{} - {}".format(title, str(pat)))
   g.map(sns.scatterplot, x="Fraction", y="FeatureChange")
   g.map(sns.lineplot, x="Fraction", y="FeatureChange")
   g.set_axis_labels("Fraction", "Feature Change")
   g.set_titles("{col_name}")

   plt.savefig(savepath + "{}_{}.png".format(title, str(pat)))
   plt.clf()