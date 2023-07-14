import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from ImageNormalisation import UsefulFunctions as UF
from tqdm import tqdm

####################################################

def MedianSignalPlot(root, Norm):
    '''
    Plot the median signal intensity for each patient within prostate in facetgrid
    '''
    
    df_fts = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Longitudinal_All_fts_Baseline.csv")

    # filter for only original_firstorder_median
    df_fts = df_fts[df_fts["Feature"] == "original_firstorder_Median"]
    # PatIDs = df_fts["PatID"].unique()

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
    plt.savefig(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Longitudinal\\SignalPlots\\MedianSignal.png")

####################################################

def ClusterSignalPlots(root, Norm, tag):
    '''
    Indivudal plots for each patient and cluster, selected features are highlighted
    '''    
    #csvs = [csv for csv in csvs if "HM" in csv]

    fts_s = pd.read_csv("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Longitudinal_SelectedFeatures_" + tag + ".csv")
    fts_s = fts_s["Feature"].values
    patIDs = UF.SABRPats()

    for pat in tqdm(patIDs):
        df = pd.read_csv("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Longitudinal\\ClusterLabels\\" + pat + "_" + tag + ".csv")
        
        df["Selected"] = df["Feature"].apply(lambda x: x in fts_s)
        # print where selected is True
        df = df[['Feature', 'Cluster', 'Fraction', 'FeatureChange', 'Selected']]
        df['Feature'] = df['Feature'].str.replace('original_', '')
        clusters = df["Cluster"].unique()
        clusters = sorted(clusters, key=lambda x: int(x))
        for c in clusters:
            df_c = df[df["Cluster"] == c]
            df_c = df_c.sort_values(by = ["Fraction"])

            # get selected features
            selected_fts = df_c[df_c["Selected"] == True]["Feature"].unique()
            if len(selected_fts) == 0:
                sf_str = "No features selected"
            
            number_fts = "Total number of features in Cluster {}: {}\nNumber of selected features: {}\n".format(c, df_c["Feature"].nunique(), len(selected_fts) )
            text_str = selected_fts
            text_str = '\n'.join(text_str)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.7)
            fts = df_c["Feature"].values
            plt.figure(figsize=(10, 10))
            plt.title(" Cluster " + str(c))
            sns.set_theme(style="whitegrid")
            sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.5})
            for ft in fts:
                df_ft = df_c[df_c["Feature"] == ft]
                values = df_ft["FeatureChange"].values
                fractions = df_ft["Fraction"].values
                colour = "blue" if df_ft["Selected"].values[0] else "grey"
                l = df_ft["Feature"].values[0]
                plt.plot(fractions, values, label = l, color = colour)
                #plt.scatter(fractions, values, color = colour)
            plt.xlabel("Fraction", fontsize = 20)
            plt.ylabel("Feature Change", fontsize = 20)
            plt.xticks(np.arange(1, 5.1, 1))
            plt.xlim(1, 5)
            #plt.ylim(-1, 1)
            # add text box
            plt.text(0.05, 0.95, (number_fts + text_str), transform=plt.gca().transAxes, fontsize=20, verticalalignment='top', bbox=props)
            
            #plt.legend(title = "Feature Selected", bbox_to_anchor=(1, 0.6), labels = ["Yes", "No"])
            plt.title("Patient - " + str(pat) + " Cluster - " + str(c), fontsize = 30)
            plt.savefig("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Longitudinal\\ClusterPlots\\" + str(pat) + "_Cluster" + str(c) + "_" + tag + ".png", bbox_inches = "tight")
            #plt.show()
            plt.close()

####################################################

def SelectedFeatures(root, Norm, tag, Model):
    '''
    Plots selected features given Norm and tag using Seaborn facet grid
    Compares different patients
    '''
    # get selected features
    fts_s = pd.read_csv("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\" + Model + "_SelectedFeatures_" + tag + ".csv")
    fts_s = fts_s["Feature"].values
    patIDs = UF.SABRPats()
    df_all = pd.read_csv("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Longitudinal_All_fts_" + tag + ".csv")
    df_all = df_all[df_all["Feature"].isin(fts_s)]

    g = sns.FacetGrid(df_all, col="Feature", col_wrap=4, height=2, aspect=1.5)
    # set color palette
    g = g.map_dataframe(sns.lineplot, x="Fraction", y="FeatureValue", hue="PatID", palette = "pastel", markers=True, dashes=False)
    # dont share y axis
    
    g.set_axis_labels("Fraction", "Feature Change", fontsize=16)
    # change fontsize of x and y labels
    # change fontsize of x and y ticks
    plt.tick_params(labelsize=16)
    # set title of total figure
    g.fig.suptitle("Selected Features", fontsize=30, y=1.0)
    g.figure.subplots_adjust(top=0.9)
    g.set_titles("{col_name}")
    g.add_legend()
    g.legend.set_title("Patient")
    g.legend.set_bbox_to_anchor((1.1, 0.5))
    
    plt.savefig(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Longitudinal\\SignalPlots\\SelectedFeatures2_" + tag + ".png")

####################################################

def CompareNormBarPlot(root, tag):
    '''
    Plots the number of features removed / selected for each Normalisation
    '''
    Norms = UF.NormArray()

    # loop through norms and get number of features removed / selected
    df = pd.DataFrame(columns = ["Norm", "Stage", "Features"])
    for Norm in Norms:
        fts_s = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\OldFeatureFiles\\" + Norm + "\\Features\\Longitudinal_SelectedFeatures.csv")
        fts_s = fts_s["Feature"].values
        fts_vol = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\OldFeatureFiles\\" + Norm + "\\Features\\Longitudinal_FeaturesRemoved_Volume.csv")
        fts_vol = fts_vol["Feature"].values
        fts_icc = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\OldFeatureFiles\\" + Norm + "\\Features\\Longitudinal_RemovedFeatures_ICC.csv")
        fts_icc = fts_icc["Feature"].values
        df = df.append({"Norm": Norm, "Stage": "Volume", "Features": len(fts_vol)}, ignore_index = True)
        df = df.append({"Norm": Norm, "Stage": "ICC", "Features": len(fts_icc)}, ignore_index = True)
        df = df.append({"Norm": Norm, "Stage": "Selected", "Features": len(fts_s)}, ignore_index = True)

    # plot
    sns.set_theme(style="whitegrid")
    sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 2.5})
    plt.figure(figsize=(10, 10))
    sns.barplot(x="Norm", y="Features", hue="Stage", data=df)
    plt.title("Number of Features Removed / Selected", fontsize = 30)
    plt.xlabel("Normalisation", fontsize = 20)
    plt.ylabel("Number of Features", fontsize = 20)
    plt.show()