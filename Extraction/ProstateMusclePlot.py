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
url = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\Datafiles\\SABR.csv"

# output directories for plots
out_20f = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\\\20fractions\\"
out_20f_new = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions_new\\"
out_SABR = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR\\"
out_SABR_new = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR_new\\"

output = out_SABR

df = pd.read_csv(url)

patIDs = df.PatID.unique()
print(patIDs)

Obs = df.Observer.unique()
rgb_vals = sns.color_palette("colorblind", len(Obs))
colourmap = dict(zip(Obs, rgb_vals))
#df["Mean Muscle"] = np.random.randint(50,100)



for i in patIDs:
    print("Processing patient: " + str(i))
    patient = [i]

    fig = plt.figure(figsize=(7,5))
    plt.title("Mean MR signal - Patient: " + str(i))
    plt.xlabel("MR Scan")
    plt.ylabel("Signal Intensity")
    plt.ylim(0,130)

    temp_df = df[df["PatID"].isin(patient)]
    temp_df = temp_df.sort_values(by="Scan")

    Timepoints = df.ScanDate.unique()

    plot = sns.scatterplot(x="Scan", y="Mean", hue="Observer", style="Region", palette=colourmap,data=temp_df)
    
    plt.xticks(Timepoints)
    plt.legend(loc="lower right")
    fig.savefig(output + str(i) + ".png", dpi=300)
    print("-------------------------------------")

