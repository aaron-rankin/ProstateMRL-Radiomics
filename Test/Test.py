import pandas as pd
import scipy.cluster.hierarchy as spch
import os
from tqdm import tqdm
import numpy as np
from scipy import stats
patIDs = ['653', '713', '752', '826', '1088', '1089', '1118', '1303', '1307', '1464', '1029',
 '1302', '1431', '1481', '1540', '1553', '1601', '1642', '829', '955']


def DistanceMatrix(DataRoot, Norm, output):
    '''
    Calculates Eucledian distance between all features for each patient
    '''
    root = DataRoot
    df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Longitudinal_All_fts.csv")

    fts_ICC = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Longitudinal_FeaturesRemoved_ICC.csv")
    fts_Vol = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Longitudinal_FeaturesRemoved_Volume.csv")

    df_all = df_all[~df_all["Feature"].isin(fts_ICC["Feature"])]
    df_all = df_all[~df_all["Feature"].isin(fts_Vol["Feature"])]

    patIDs = df_all["PatID"].unique()
    fts = df_all["Feature"].unique()

    print("Volume Redundant features: {}".format(len(fts_Vol)))
    print("ICC Redundant features: {}".format(len(fts_ICC)))
    print("Remainder of features: {}".format(len(fts)))

    df_all = RescaleFeatures(df_all)
    # loop through patients

    for pat in tqdm(patIDs):
        df_pat = df_all[df_all["PatID"] == pat]

        # empty matrix
        mat = np.zeros((len(fts), len(fts)))

        for ft1 in range(len(fts)):
            vals_ft1 = df_pat[df_pat["Feature"] == fts[ft1]]["FeatureChange"].values

            for ft2 in range(len(fts)):
                vals_ft2 = df_pat[df_pat["Feature"] == fts[ft2]]["FeatureChange"].values

                # calculate correlation
                mat[ft1, ft2] = stats.pearsonr(vals_ft1, vals_ft2)[0]

        # save matrix
        df_dist = pd.DataFrame(mat, columns = fts, index = fts)  
        df_dist.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm +"\\Longitudinal\\Test\\DM\\csvs\\" + str(pat) + "_Rescaled.csv")

        # plot matrix
        #plt.figure(figsize=(20,20))
        #sns.set_theme(style="white")
        #plt.title("DM - {}".format(pat), fontsize=40)
        #sns.heatmap(df_dist, cmap='viridis', cbar_kws={'label': 'Euclidean Distance'})
        #plt.savefig(root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\"+ Norm +"\\Longitudinal\\Test\\DM\\Figs\\" + str(pat) + ".png")

#ClusterFeatures("E:\\", "HM-FS", 2, False)

def RescaleFeatures(df):
        '''
        Rescales features to be between 0 and 1
        '''
        df = df.copy()
        for ft in df["Feature"].unique():
                vals = df[df["Feature"] == ft]["FeatureChange"].values
                df.loc[df["Feature"] == ft, "FeatureChange"] = (vals - min(vals)) / (max(vals) - min(vals))

        return df

DistanceMatrix("E:\\", "HM-FS", True)