"""""

Aaron Rankin 08/03/22
Reads in csv with mean and std of MR signal from prostate contours and msucle clicks
Plots values

"""""

from random import randint
from cv2 import rotate
import numpy as np
import pandas as pd
from scipy import rand
import seaborn as sns
import matplotlib.pyplot as plt

# load in csv -- Change according to dataset
url = "\\\\130.88.233.166\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\Datafiles\\20fractions.csv"

# output directories for plots
out_20f = "\\\\130.88.233.166\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\\\20fractions\\"
out_20f_new = "\\\\130.88.233.166\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions_new\\"
out_SABR = "\\\\130.88.233.166\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR\\"
out_SABR_new = "\\\\130.88.233.166\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR_new\\"

output = out_20f

df = pd.read_csv(url)

patIDs = df.PatID.unique()
print(patIDs.size)
print(patIDs)

Obs = df.Observer.unique()
rgb_vals = sns.color_palette("colorblind", len(Obs))
colourmap = dict(zip(Obs, rgb_vals))
df["Mean Muscle"] = np.random.randint(50,100)
print(df)

for i in patIDs:
    print("Processing patient: " + str(i))
    patient = [i]

    fig = plt.figure(figsize=(7,5))
    plt.title("Mean MR signal - Patient: " + str(i))
    plt.xlabel("MR Scan")
    plt.ylabel("Signal Intensity")
    plt.ylim(0,110)

    temp_df = df[df["PatID"].isin(patient)]
    temp_df = temp_df.sort_values(by="Scan")
    timepoints = temp_df.Scan.unique()

    plot_pros = sns.scatterplot(x="Scan", y="Mean Prostate", hue="Observer",palette=colourmap,data=temp_df)
    plot_musc = sns.scatterplot(x="Scan", y="Mean Muscle", data=temp_df)
    plt.legend(loc="lower right")
    fig.savefig(output + str(i) + ".png", dpi=300)
    print("-------------------------------------")

# plt.figure("Mean Intensity Plot")
# plt.title("Mean Signal Intensity Patient: " + i)
# plt.ylabel("MR Intensity")
# plt.xlabel("MR Scan")


# plt.scatter(x=Timepoints, y=ProsContourMeans)
# print(ProsContourMeans)            
# # outputfolder = output + i
# # if not os.path.exists(outputfolder):
# #     os.mkdir(outputfolder)
# # else:
# #     print()
# # plt.hist(imageArray, bins = 256, range=(1, imageArray.max()), facecolor = "blue", alpha = 0.75, color = "black", fill = False, histtype = "step", density = True, label = "WholeImage")
# # plt.legend()
# plt.savefig(output + str(i) + ".png", dpi = 300)
# plt.clf()

