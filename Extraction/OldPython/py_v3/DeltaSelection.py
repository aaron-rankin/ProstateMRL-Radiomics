import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# read csv file
df = pd.read_csv("C:\\Users\\b01297ar\\Documents\\ProstateMRL-local\\ProstateMRL-Radiomics\\Data\\Delta\\Delta_fts_corr.csv")
# loop through all fts and select fts with correlation > 0.5
# get column names
fts = df["Unnamed: 0"].values
print(df.head())
# convert to numpy array
array = df.to_numpy()

# remove index and cokumn names
array = array[:,1:]
# create a new array to store the results
results = np.empty((len(fts), len(fts)))
selected_ft_pairs = []
for i in range(len(fts)):
    # if value is > 0.5, print the feature name

    for j in range(len(fts)):
        if array[i,j] < 0.5:
            #df = np.delete(df, j, 0)
            results[i,j] = array[i,j]
            selected_ft_pairs.append([fts[i], fts[j]])

        
        else:
            results[i,j] = 1

results = pd.DataFrame(results, index=fts, columns=fts)
# plot heatmap
plt.figure(figsize=(20, 20))
sns.heatmap(results, cmap="YlGnBu")
plt.savefig("C:\\Users\\b01297ar\\Documents\\ProstateMRL-local\\ProstateMRL-Radiomics\\Data\\Delta\\Delta_fts_corr_0.5.png")

# loop through results with ft pairs and select ft with lowest mean value
# create an empty array to store the results
fts_keep = []
fts_remove = []
for i in range(len(selected_ft_pairs)):
    # print(selected_ft_pairs[i])
    # select ft pair
    df_ft1 = df[df["Unnamed: 0"] == selected_ft_pairs[i][0]]
    # print(df_ft1)
    df_ft2 = df[df["Unnamed: 0"] == selected_ft_pairs[i][1]]
    # get mean values across row
    mean_ft1 = float(df_ft1.mean(axis=1))
    mean_ft2 = float(df_ft2.mean(axis=1))

    # compare mean values
    if mean_ft1 < mean_ft2:
        fts_keep.append(selected_ft_pairs[i][0])
        fts_remove.append(selected_ft_pairs[i][1])
    else:
        fts_keep.append(selected_ft_pairs[i][1])
        fts_remove.append(selected_ft_pairs[i][0])
    
# remove duplicates
fts_keep = list(dict.fromkeys(fts_keep))
fts_remove = list(dict.fromkeys(fts_remove))

# compare lists
fts_remove = [x for x in fts_remove if x not in fts_keep]
fts_keep = [x for x in fts_keep if x not in fts_remove]


# read in ft dataframe
df_fts = pd.read_csv("C:\\Users\\b01297ar\\Documents\\ProstateMRL-local\\ProstateMRL-Radiomics\\Data\\Delta\\Delta_fts.csv")
# select fts to if in fts_keep
df_fts = df_fts[df_fts["FeatureName"].isin(fts_keep)]

# save to csv
df_fts = df_fts.drop(columns=["Unnamed: 0"])
df_fts.to_csv("C:\\Users\\b01297ar\\Documents\\ProstateMRL-local\\ProstateMRL-Radiomics\\Data\\Delta\\Delta_fts_selected.csv", index=False)


