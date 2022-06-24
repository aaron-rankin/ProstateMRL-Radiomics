import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os


Treatment = "SABR" #SABR
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
        rgb_vals = sns.color_palette("colorblind", len(Norms))
        colourmap = dict(zip(Norms, rgb_vals))

        sns.set_theme(style='darkgrid')
        fig, axes = plt.subplots(1,3,sharex=False,figsize=(20,8))

        plt.xlabel("Days from Fraction 1")   
        plt.ylabel("Signal")
        fig.suptitle("Patient - " + str(patID), fontsize=30)

        pros_df = pat_df.loc[pat_df["Region"] == "Prostate"]
        axes[0].set_title("Prostate Signal Change", fontsize=20)
        axes[0].set_xlabel("Days From Fraction 1")
        #axes[0,0].set_ylabel("Mean Signal")
        #pros_1 = sns.lineplot(data=pros_df, ax=axes[0,0], x="DaysDiff", y="MeanSignal", hue="Normalisation", palette=colourmap, legend=False)
        #pros_2 = sns.scatterplot(data=pros_df, ax=axes[0,0],  x="DaysDiff", y="MeanSignal", hue="Normalisation", palette=colourmap, legend=False)
        #axes[0,1].set_title("Prostate Change", fontsize=20)
        #axes[0,1].set_xlabel("Days From Fraction 1")
        axes[0].set_ylabel("Mean Signal Change")
        pros_3 = sns.lineplot(data=pros_df, ax=axes[0], x="DaysDiff", y="MeanDiff", hue="Normalisation", palette=colourmap, legend=False)
        pros_4 = sns.scatterplot(data=pros_df, ax=axes[0],  x="DaysDiff", y="MeanDiff", hue="Normalisation", palette=colourmap, legend=False)
        
        psoas_df = pat_df.loc[pat_df["Region"] == "Psoas"]
        axes[1].set_title("Psoas Signal Change", fontsize = 20)
        axes[1].set_xlabel("Days From Fraction 1")
        #axes[1,0].set_ylabel("Mean Signal")
        #psoas_1 = sns.lineplot(data=psoas_df, ax=axes[1,0], x="DaysDiff", y="MeanSignal", hue="Normalisation", palette=colourmap, legend=False)
        #psoas_2 = sns.scatterplot(data=psoas_df, ax=axes[1,0],  x="DaysDiff", y="MeanSignal", hue="Normalisation", palette=colourmap, legend=False)
        #axes[1,1].set_title("Psoas Change", fontsize = 20)

        #axes[1,1].set_xlabel("Days From Fraction 1")
        axes[1].set_ylabel("Mean Signal Change")
        psoas_3 = sns.lineplot(data=psoas_df, ax=axes[1], x="DaysDiff", y="MeanDiff", hue="Normalisation", palette=colourmap, legend=False)
        psoas_4 = sns.scatterplot(data=psoas_df, ax=axes[1],  x="DaysDiff", y="MeanDiff", hue="Normalisation", palette=colourmap, legend=False)
        
        glute_df = pat_df.loc[pat_df["Region"] == "Glute"]
        axes[2].set_title("Glute Signal Change", fontsize=20)
        axes[2].set_xlabel("Days From Fraction 1")
        #axes[1,0].set_ylabel("Mean Signal")
        #glute_1 = sns.lineplot(data=glute_df, ax=axes[0,2], x="DaysDiff", y="MeanSignal", hue="Normalisation", palette=colourmap, legend=False)
        #glute_2 = sns.scatterplot(data=glute_df, ax=axes[0,2],  x="DaysDiff", y="MeanSignal", hue="Normalisation", palette=colourmap, legend=False)
        #axes[2,1].set_title("Glute Change", fontsize=20)
        #axes[2,1].set_xlabel("Days From Fraction 1")
        axes[2].set_ylabel("Mean Signal Change")
        glute_3 = sns.lineplot(data=glute_df, ax=axes[2], x="DaysDiff", y="MeanDiff", hue="Normalisation", palette=colourmap, legend=False)
        glute_4 = sns.scatterplot(data=glute_df, ax=axes[2],  x="DaysDiff", y="MeanDiff", hue="Normalisation", palette=colourmap, legend=False)

        labels_plot = fig.axes[-1].get_legend_handles_labels()
        fig.legend()#(loc=1, bbox_to_anchor=(1.25, 0.5), ncol=1, title="Normalisation")
        sns.move_legend(fig, labels=glute_df.Normalisation.unique(),loc="center right", ncol=1, title="Normalisation", frameon=True)
        #fig.tight_layout()
        fig.savefig("D:\\data\\Aaron\\ProstateMRL\\Data\\MRLPacks\\Test\\" + patID + "_1.png", dpi=300)    
        print("-------------------------------------")
        plt.clf()
