import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os


#Treatment = "SABR" #SABR
all_df = os.scandir("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges\\")
#print(all_df.head())

#patIDs = all_df.PatID.unique()

#plt.ylim(-120,270)

for i in all_df:
    #print(i.name)
    patID = i.name[:-4]
    if "test" in patID:
        #print(patID)
        pat_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges\\" + patID + ".csv")
        print(pat_df.head())
        patID = patID[:-5]
        

        Norms = pat_df.Normalisation.unique()
        Regions = pat_df.Region.unique()
        rgb_vals = sns.color_palette("colorblind", len(Regions))
        colourmap = dict(zip(Regions, rgb_vals))

        sns.set_theme(style='darkgrid')
        fig, axes = plt.subplots(3,2,sharex=False,figsize=(15,15))

        plt.xlabel("Days from Fraction 1")   
        plt.ylabel("Signal")
        fig.suptitle("Patient - " + str(patID), fontsize=30)

        df = pat_df.loc[pat_df["Normalisation"] == Norms[0]]
        axes[0,0].set_title(Norms[0], fontsize=16)
        axes[0,0].set_xlabel(" ")#("Days From Fraction 1")
        axes[0,0].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[0,0], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[0,0],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == Norms[1]]
        axes[0,1].set_title(Norms[1], fontsize=16)
        axes[0,1].set_xlabel(" ")#("Days From Fraction 1")
        axes[0,1].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[0,1], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[0,1],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == Norms[2]]
        axes[1,0].set_title(Norms[2], fontsize=16)
        axes[1,0].set_xlabel(" ")#("Days From Fraction 1")
        axes[1,0].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[1,0], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[1,0],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == Norms[3]]
        axes[1,1].set_title(Norms[3], fontsize=16)
        axes[1,1].set_xlabel(" ")#("Days From Fraction 1")
        axes[1,1].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[1,1], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[1,1],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == Norms[4]]
        axes[2,0].set_title(Norms[4], fontsize=16)
        axes[2,0].set_xlabel("Days From Fraction 1")
        axes[2,0].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[2,0], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[2,0],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == Norms[5]]
        axes[2,1].set_title(Norms[5], fontsize=16)
        axes[2,1].set_xlabel("Days From Fraction 1")
        axes[2,1].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[2,1], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[2,1],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
    
        labels_plot = fig.axes[-1].get_legend_handles_labels()
        fig.legend()#(loc=1, bbox_to_anchor=(1.25, 0.5), ncol=1, title="Normalisation")
        sns.move_legend(fig, labels=df.Region.unique(),loc="lower center", ncol=3, title="Region", frameon=True)
        #fig.tight_layout()
        fig.savefig("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Test\\" + patID + "_2.png", dpi=300)    
        print("-------------------------------------")
        plt.clf()
