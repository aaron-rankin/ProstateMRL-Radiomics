import os
import pandas as pd

dir = os.listdir("E:\\Aaron\\ProstateMRL\\Data\\Paper1\\HM-FSTP\\Longitudinal\\ClusterLabels\\")

df_result = pd.DataFrame()

for f in dir:

    df = pd.read_csv("E:\\Aaron\\ProstateMRL\\Data\\Paper1\\HM-FSTP\\Longitudinal\\ClusterLabels\\" + f)
    #print(f[3:-4])
    df = df[["Feature", "Cluster"]]
    # remove duplicates
    df = df.drop_duplicates()
    # sort by cluster
    df = df.sort_values(by=["Cluster"])
    cluster_num = df["Cluster"].unique()
    # turn value counts into a dataframe
    df = df["Cluster"].value_counts().rename_axis("Cluster").reset_index(name="Counts")
    # set PatID as index
    df["PatID"] = f[3:-4]
    # set PatID as index
    df.set_index("PatID", inplace=True)
        
    # append to result
    df_result = df_result.append(df, ignore_index=False)

        # get total number of clusters
        #print(df)
        #print(cluster_num)

# Get mean number of clusters per patient
#print(df_result["Counts"].mean())

#  get max number of clusters per patient
#print(df_result)

df_numclust= df_result.groupby("PatID")["Cluster"].max()
df_numclust = df_numclust.rename_axis("PatID").reset_index(name="NumClusters")

# get mean number of clusters per patient
#print(df_numclust)

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
print(df_numclust, "\n")

print("Mean number of cluster per patient: ", df_numclust["NumClusters"].mean())
print("Median number of cluster per patient: ", df_numclust["NumClusters"].median())

print("Mean fts over all clusters: ", meanftscluster)
print("Median fts over all clusters: ", medianftscluster)

print("Mean mean fts per cluster per patient: ", df_numfts["MeanFeaturesperCluster"].mean())
print("Median mean fts per cluster per patient: ", df_medianfts["MedianFeaturesperCluster"].median())

