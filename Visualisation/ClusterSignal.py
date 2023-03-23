import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
Norm = "HM-FS"

csvs = os.listdir("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Longitudinal\ClusterLabels2\\")
#csvs = [csv for csv in csvs if "HM" in csv]

fts_s = pd.read_csv("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Longitudinal_SelectedFeatures2.csv")
fts_s = fts_s["Feature"].values
for csv in tqdm(csvs):
    df = pd.read_csv("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Longitudinal\\Test\\ClusterLabels\\" + csv)
    pat = str(csv)[:-4]
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
        plt.savefig("E:\\Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Longitudinal\\Test\\ClusterPlots\\" + str(pat) + "_Cluster" + str(c) + "_RS.png", bbox_inches = "tight")
        #plt.show()
        plt.close()




