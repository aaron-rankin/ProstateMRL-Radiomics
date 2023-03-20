import pandas as pd
import scipy.cluster.hierarchy as spch
import os


def ClusterCheck(df, t_val, df_DM):
        df_c = df
        df_new = pd.DataFrame()
        # feature names
        df_new["FeatureName"] = df_c.index
        # cluster labels
        c = df_c["Cluster"].values[0]
        
        # need to filter distance matrix to only include features in cluster
        df_DM_c = df_DM[df_c.index]
        # only keep features in cluster
        df_DM_c = df_DM_c[df_DM_c.index.isin(df_c.index)]
        
        # convert to numpy array
        arr_DM_c = df_DM_c.to_numpy()
        
        # cluster
        df_new["Cluster"] = spch.fclusterdata(arr_DM_c, t=t_val, criterion="distance", method="ward")
        df_new["Cluster"] = c*100 + df_new["Cluster"]
        df_new["Cluster"] = df_new["Cluster"].astype(int)
        df_new["NumFts"] = df_new.groupby("Cluster")["Cluster"].transform("count")
        number_fts = df_new["NumFts"].unique()
        #print(t_val, number_fts)#, df_new)
        return number_fts, df_new


def ClusterFeatures(DM_dir):
        t_val = 2
        cluster_method = "ward"
        df_DM = pd.read_csv(DM_dir)
        df_DM.set_index("Unnamed: 0", inplace=True)
        arr_DM = df_DM.to_numpy()
        fts = df_DM.columns

        # create temp df to hold ft name and label
        df_labels = pd.DataFrame()
        df_labels["FeatureName"] = fts

        # cluster function using DM, need to experiment with t_val and method
        df_labels["Cluster"] = spch.fclusterdata(arr_DM, t=t_val, criterion="distance", method=cluster_method)
        df_labels.set_index("FeatureName", inplace=True)
        
        # check number of features in each cluster
        df_labels["NumFts"] = df_labels.groupby("Cluster")["Cluster"].transform("count")
        df_labels["Cluster"] = df_labels["Cluster"].astype(int)
        print(df_labels.loc[df_labels["NumFts"] > 10])
        # loop through clusters 
        for c in df_labels["Cluster"].unique():
                df_c = df_labels[df_labels["Cluster"] == c]
                number_fts = len(df_c)

                # check numnber of features in cluster
                if number_fts > 10:
                        print("Cluster: {} Number of Features: {}".format(c, number_fts)) 
                        t_val = 1.8
                        # if more than 10 features in cluster, reduce t_val and recluster
                        number_fts, df_labels2= ClusterCheck(df_c, t_val, df_DM)
                        tries = 0
                        while number_fts.max() > 10:
                                t_val = t_val - 0.2
                                tries += 1
                                print("Tries: {} T_val: {}".format(tries, t_val))
                                number_fts, df_labels2 = ClusterCheck(df_c, t_val, df_DM)
                                
                        print(df_labels2)
                        new_fts = df_labels2["FeatureName"].unique()
                        df_labels.loc[new_fts, "Cluster"] = df_labels2["Cluster"].values
                        df_labels["NumFts"] = df_labels.groupby("Cluster")["Cluster"].transform("count")



csvs = os.listdir("E:\\Aaron\\ProstateMRL\\Data\\Paper1\\HM-FS\\Longitudinal\\DM\\csvs\\")
#test_DM = "E:\\Aaron\\ProstateMRL\\Data\\Paper1\\HM-FS\\Longitudinal\\DM\\csvs\\752.csv"

for csv in csvs:
        test_DM = "E:\\Aaron\\ProstateMRL\\Data\\Paper1\\HM-FS\\Longitudinal\\DM\\csvs\\" + csv
        print("-----------------------------------------------------------------")
        print("Patient: {}".format(csv[:-4]))
        print("-----------------------------------------------------------------")
        ClusterFeatures(test_DM)