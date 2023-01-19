import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os


#Treatment = "SABR" #SABR
csvs = os.scandir("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges_v2\\")
#print(all_df.head())

#patIDs = all_df.PatID.unique()

#plt.ylim(-120,270)

for i in csvs:
    print(i.name)
    file = i.name[:-4]
    patID = file.split("_")[0]

    #print(patID)
    pat_df = pd.read_csv("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\InterFractionChanges_v2\\" + file + ".csv")
    
    Norms = pat_df.Normalisation.unique()
    Regions = pat_df.Region.unique()
    rgb_vals = sns.color_palette("colorblind", len(Regions))
    colourmap = dict(zip(Regions, rgb_vals))

    if len(Norms) == 6:

        sns.set_theme(style='darkgrid')
        fig, axes = plt.subplots(2,3,sharex=False,figsize=(25,15))

        plt.xlabel("Days from Fraction 1")   
        plt.ylabel("Signal")
        fig.suptitle("Patient - " + str(patID), fontsize=30)

        df = pat_df.loc[pat_df["Normalisation"] == "Raw"]
        axes[0,0].set_title("Raw", fontsize=16)
        axes[0,0].set_xlabel("Days From Fraction 1")
        axes[0,0].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[0,0], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[0,0],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == "HM-TP"]
        axes[0,1].set_title("HM-TP", fontsize=16)
        axes[0,1].set_xlabel("Days From Fraction 1")
        axes[0,1].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[0,1], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[0,1],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == "HM-FS"]
        axes[0,2].set_title("HM-FS", fontsize=16)
        axes[0,2].set_xlabel("Days From Fraction 1")
        axes[0,2].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[0,2], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[0,2],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == "Norm-Pros"]
        axes[1,0].set_title("Mean-Pros", fontsize=16)
        axes[1,0].set_xlabel("Days From Fraction 1")
        axes[1,0].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[1,0], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[1,0],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == "Norm-Glute"]
        axes[1,1].set_title("Mean-Glute", fontsize=16)
        axes[1,1].set_xlabel("Days From Fraction 1")
        axes[1,1].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[1,1], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[1,1],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == "Norm-Psoas"]
        axes[1,2].set_title("Mean-Psoas", fontsize=16)
        axes[1,2].set_xlabel("Days From Fraction 1")
        axes[1,2].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[1,2], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[1,2],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        '''
        df = pat_df.loc[pat_df["Normalisation"] == "Med-Pros"]
        axes[2,0].set_title("Med-Pros", fontsize=16)
        axes[2,0].set_xlabel("Days From Fraction 1")
        axes[2,0].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[2,0], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[2,0],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == "Med-Glute"]
        axes[2,1].set_title("Med-Glute", fontsize=16)
        axes[2,1].set_xlabel("Days From Fraction 1")
        axes[2,1].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[2,1], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[2,1],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)

        df = pat_df.loc[pat_df["Normalisation"] == "Med-Psoas"]
        axes[2,2].set_title("Med-Psoas", fontsize=16)
        axes[2,2].set_xlabel("Days From Fraction 1")
        axes[2,2].set_ylabel("Mean Signal Change")
        plot_1 = sns.lineplot(data=df, ax=axes[2,2], x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        plot_2 = sns.scatterplot(data=df, ax=axes[2,2],  x="DaysDiff", y="MeanDiff", hue="Region", palette=colourmap, legend=False)
        '''
        labels_plot = fig.axes[-1].get_legend_handles_labels()
        fig.legend()#(loc=1, bbox_to_anchor=(1.25, 0.5), ncol=1, title="Normalisation")
        sns.move_legend(fig, labels=df.Region.unique(),loc="center right", ncol=1, title="Region", frameon=True)
        #fig.tight_layout()
        fig.savefig("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Test\\" + str(patID) + ".png", dpi=300)    
        print("-------------------------------------")
        plt.clf()
