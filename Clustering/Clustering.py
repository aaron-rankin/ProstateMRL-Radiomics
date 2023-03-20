import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
from scipy.cluster.hierarchy import dendrogram
import scipy.cluster.hierarchy as spch
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent + "\\Functions\\")
import UsefulFunctions as UF
import ImageFunctions as IF
from scipy.spatial import distance

def DistanceMatrix(DataRoot, Norm, output):
    root = DataRoot
    df_all = pd.read_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\Longitudinal_fts_pVol.csv")

    patIDs = df_all["PatID"].unique()
    fts = df_all["Feature"].unique()
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
                mat[ft1, ft2] = distance.euclidean(vals_ft1, vals_ft2)
        
        # save matrix
        df_dist = pd.DataFrame(mat, columns = fts, index = fts)  
        df_dist.to_csv(root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm +"\\Longitudinal\\DM\\csvs\\" + str(pat) + ".csv")

        # plot matrix
        plt.figure(figsize=(20,20))
        sns.set_theme(style="white")
        plt.title("DM - {}".format(pat), fontsize=40)
        sns.heatmap(df_dist, cmap='viridis', cbar_kws={'label': 'Euclidean Distance'})
        plt.savefig(root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\"+ Norm +"\\Longitudinal\\DM\\Figs\\" + str(pat) + ".png")


def ClusterFeatures(DataRoot, Norm, t_val, output):
    root = DataRoot
    DM_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\" + Norm + "\\Longitudinal\\DM\\csvs\\"
    out_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\"+ Norm + "\\Longitudinal\\ClusterLabels\\"

    t_val = t_val
    patIDs = UF.SABRPats()
    cluster_method = "ward"

    for pat in tqdm(patIDs):
        df_DM = pd.read_csv(DM_dir + pat + ".csv")
        df_DM.set_index("Unnamed: 0", inplace=True)
        arr_DM = df_DM.to_numpy()
        fts = df_DM.columns

        # create temp df to hold ft name and label
        df_labels = pd.DataFrame()
        df_labels["FeatureName"] = fts

        # cluster function using DM, need to experiment with t_val and method
        df_labels["Cluster"] = spch.fclusterdata(arr_DM, t=t_val, criterion="distance", method=cluster_method)
        df_labels.set_index("FeatureName", inplace=True)
        
        # read in df with ft vals and merge
        ft_vals = pd.read_csv(root +"Aaron\\ProstateMRL\\Data\\Paper1\\"+ Norm + "\\Features\\Longitudinal_fts_pVol.csv")
        ft_vals["PatID"] = ft_vals["PatID"].astype(str)
        pat_ft_vals = ft_vals[ft_vals["PatID"] == pat]
        pat_ft_vals = pat_ft_vals.merge(df_labels, left_on="Feature", right_on="FeatureName")

        # output is feature values w/ cluster labels
        pat_ft_vals.to_csv(out_dir + pat + ".csv")

def ClusterCount(root, Norm, output):
    dir = os.listdir(root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\" + Norm + "\\Longitudinal\\ClusterLabels\\")

    df_result = pd.DataFrame()

    for f in dir:
    
        df = pd.read_csv(root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\" + Norm + "\\Longitudinal\\ClusterLabels\\" + f)
        df = df[["Feature", "Cluster"]]
        df = df.drop_duplicates()
        # sort by cluster
        df = df.sort_values(by=["Cluster"])
        # turn value counts into a dataframe
        df = df["Cluster"].value_counts().rename_axis("Cluster").reset_index(name="Counts")
        # set PatID as index
        df["PatID"] = f[3:-4]
        # set PatID as index
        df.set_index("PatID", inplace=True)
            
        # append to result
        df_result = df_result.append(df, ignore_index=False)
    #get number of clusters with more than 3 features
    df_stable = df_result[df_result["Counts"] > 3]
    df_stable = df_stable.groupby("PatID")["Cluster"].count()
    # get mean number of stable clusters
    meanstable = df_stable.mean()

    df_numclust= df_result.groupby("PatID")["Cluster"].max()
    df_numclust = df_numclust.rename_axis("PatID").reset_index(name="NumClusters")

    # group by patient and get mean number of clusters
    df_numfts = df_result.groupby("PatID")["Counts"].mean()
    df_numfts = df_numfts.rename_axis("PatID").reset_index(name="MeanFeaturesperCluster")
    df_medianfts = df_result.groupby("PatID")["Counts"].median()
    df_medianfts = df_medianfts.rename_axis("PatID").reset_index(name="MedianFeaturesperCluster")

    meanftscluster = df_result["Counts"].mean()
    medianftscluster = df_result["Counts"].median()
    # get mean number of features per cluster
    #print(df_numfts)

    # merge dataframes
    df_numclust = pd.merge(df_numclust, df_numfts, on="PatID")
    df_numclust = pd.merge(df_numclust, df_medianfts, on="PatID")

    if output == True:
        print("Mean number of stable clusters per patient: ", meanstable)
        print("Mean number of clusters per patient: ", df_numclust["NumClusters"].mean())
        print("Mean features per cluster per patient: ", df_numfts["MeanFeaturesperCluster"].mean())


def ClusterSelection(DataRoot, Norm, output):
    root = DataRoot
    patIDs = UF.SABRPats()

    labels_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\" + Norm + "\\Longitudinal\\ClusterLabels\\"
    out_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\"+ Norm +"\\Features\\"
    # t val specifies threshold used for hierarchical clustering distance - needs a sensitivity test
    t_val = 2
    df_result = pd.DataFrame()
    for pat in tqdm(patIDs):
        # read in feature vals and associated cluster labels
        df_pat = pd.read_csv(labels_dir + pat + ".csv")

        cluster_num = df_pat["Cluster"].max()
        fts_selected = []
        df_result_pat = pd.DataFrame()

        # for each patient loop through each cluster to get 'best' feature
        for c in range(1, cluster_num):
            df_cluster = df_pat[df_pat["Cluster"] == c]

            # function loops through each cluster and gets feature values
            # performs cross-correlation and returns feature with highest mean correlation to all other features
            # returns NULL if < 3 features in cluster 
            ft_selected = UF.ClusterFtSelection2(df_cluster)

            if ft_selected != 0:
                for f in ft_selected:
                    fts_selected.append(f)
        
        # filter through all feature values and select only new features
            row = {}

        for f in fts_selected:
            row["patID"] = pat
            row["Feature"] = f
            df_result_pat = df_result_pat.append(row, ignore_index=True)
        
        df_result = df_result.append(df_result_pat, ignore_index=True)

    df_result = df_result.Feature.value_counts().rename_axis("Feature").reset_index(name="Counts")
    # get number of counts at 10th row
    counts = df_result.iloc[10]["Counts"]

    # get features with counts >= counts
    fts = df_result[df_result["Counts"] >= counts]["Feature"].values
    if output == True:
        print("\nSelected Features: ({})".format(len(fts)))
        for f in fts:
            print(f)
    df_result = df_result[df_result["Counts"] >= counts]

    # drop counts
    df_result.drop(columns=["Counts"], inplace=True)
    df_result.to_csv(out_dir + "Longitudinal_SelectedFeatures.csv")

