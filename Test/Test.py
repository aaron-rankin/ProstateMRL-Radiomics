import pandas as pd
import scipy.cluster.hierarchy as spch
import os
from tqdm import tqdm

patIDs = ['653', '713', '752', '826', '1088', '1089', '1118', '1303', '1307', '1464', '1029',
 '1302', '1431', '1481', '1540', '1553', '1601', '1642', '829', '955']


def ClusterCheck(df, fts, t_val, tries, df_DM):
        df_c = df
        df_new = pd.DataFrame()
        # feature names
        df_new["FeatureName"] = fts
        # cluster labels
        c = df_c["Cluster"].values[0]
        
        # need to filter distance matrix to only include features in cluster
        df_DM_c = df_DM[fts]
        # only keep features in cluster
        df_DM_c = df_DM_c[df_DM_c.index.isin(fts)]
        
        # convert to numpy array
        arr_DM_c = df_DM_c.to_numpy()
        
        # cluster
        df_new["Cluster"] = spch.fclusterdata(arr_DM_c, t=t_val, criterion="distance", method="ward")
        df_new["Cluster"] = str(c) + str(tries) + df_new["Cluster"].astype(str)
        df_new["Cluster"] = df_new["Cluster"].astype(int)
        df_new["NumFts"] = df_new.groupby("Cluster")["Cluster"].transform("count")
        number_fts = df_new["NumFts"].unique()
        fts_check = df_new.loc[df_new["NumFts"] > 10]["FeatureName"].values
        #print(t_val, number_fts)#, df_new)
        return number_fts, df_new, fts_check


def ClusterFeatures(DataRoot, Norm, s_t_val, output):
    root = DataRoot
    DM_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\" + Norm + "\\Longitudinal\\DM\\csvs\\"
    out_dir = root + "\\Aaron\\ProstateMRL\\Data\\Paper1\\"+ Norm + "\\Longitudinal\\ClusterLabels2\\"

    patIDs = ['653', '713', '752', '826', '1088', '1089', '1118', '1303', '1307', '1464', '1029',
 '1302', '1431', '1481', '1540', '1553', '1601', '1642', '829', '955']

    cluster_method = "weighted"

    for pat in tqdm(patIDs):
        df_DM = pd.read_csv(DM_dir + pat + ".csv")
        df_DM.set_index("Unnamed: 0", inplace=True)
        arr_DM = df_DM.to_numpy()
        fts = df_DM.columns

        # create temp df to hold ft name and label
        df_labels = pd.DataFrame()
        df_labels["FeatureName"] = fts

        # cluster function using DM, need to experiment with t_val and method
        df_labels["Cluster"] = spch.fclusterdata(arr_DM, t=s_t_val, criterion="distance", method=cluster_method)
        df_labels.set_index("FeatureName", inplace=True)
        
        # check number of features in each cluster
        df_labels["NumFts"] = df_labels.groupby("Cluster")["Cluster"].transform("count")
        df_labels["Cluster"] = df_labels["Cluster"].astype(int)
        print("---------------------------")
        print("Patient: {}".format(pat))
        print(df_labels.loc[df_labels["NumFts"] > 10])
        # loop through clusters 
        for c in df_labels["Cluster"].unique():
                df_c = df_labels[df_labels["Cluster"] == c]
                number_fts = len(df_c)
                # check numnber of features in cluster
                if number_fts > 10:
                        # if more than 10 features in cluster, reduce t_val and recluster
                        t_val = s_t_val - 0.2
                        check_fts = df_c.index.values
                        tries = 1
                        number_fts, df_labels2, check_fts = ClusterCheck(df_c, check_fts, t_val, tries, df_DM)
                        new_fts = df_labels2["FeatureName"].unique()
                        df_labels.loc[new_fts, "Cluster"] = df_labels2["Cluster"].values
                        df_labels["NumFts"] = df_labels.groupby("Cluster")["Cluster"].transform("count")

                        while number_fts.max() > 10:
                                t_val = t_val - 0.2
                                tries += 1
                                print("Cluster: {} Tries: {} T_val: {}".format(c, tries, t_val))
                                number_fts, df_labels2, check_fts = ClusterCheck(df_c, check_fts, t_val, tries, df_DM)
                                new_fts = df_labels2["FeatureName"].unique()
                                df_labels.loc[new_fts, "Cluster"] = df_labels2["Cluster"].values
                        
        df_labels["NumFts"] = df_labels.groupby("Cluster")["Cluster"].transform("count")

        print(df_labels)


        # read in df with ft vals and merge
        ft_vals = pd.read_csv(root +"Aaron\\ProstateMRL\\Data\\Paper1\\"+ Norm + "\\Features\\Longitudinal_fts_pVol.csv")
        ft_vals["PatID"] = ft_vals["PatID"].astype(str)
        pat_ft_vals = ft_vals[ft_vals["PatID"] == pat]
        pat_ft_vals = pat_ft_vals.merge(df_labels, left_on="Feature", right_on="FeatureName")

        # output is feature values w/ cluster labels
        pat_ft_vals.to_csv(out_dir + pat + ".csv")


ClusterFeatures("E:\\", "HM-FS", 2, False)