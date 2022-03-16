"""""

Aaron Rankin 08/03/22
Reads in csv with mean and std of MR signal from prostate contours and msucle clicks
Plots values

"""""

import enum
from random import randint
from cv2 import rotate
import numpy as np
import pandas as pd
from scipy import rand
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
# load in csv -- Change according to dataset
url = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\Datafiles\\20fractions.csv"

# output directories for plots
out_20f = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\\\20fractions\\"
out_20f_new = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions_new\\"
out_SABR = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR\\"
out_SABR_new = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR_new\\"

output = out_20f

df = pd.read_csv(url)

patIDs = df.PatID.unique()
print(patIDs)

Obs = df.Observer.unique()
rgb_vals = sns.color_palette("colorblind", len(Obs))
colourmap = dict(zip(Obs, rgb_vals))
#df["Mean Muscle"] = np.random.randint(50,100)

max_signal = df.Mean.max()

for i in patIDs:
    print("Processing patient: " + str(i))

    fig = plt.figure(figsize=(7,10))
    plt.title("Mean MR signal - Patient: " + str(i))
    plt.xlabel("Days from Fraction 1")

    plt.xlim(-2, 35)
    plt.xticks(np.arange(0,32,5))

    temp_df = df[df["PatID"].isin([i])]
    temp_df["ScanDate"] = pd.to_datetime(temp_df["ScanDate"], dayfirst=True) 
    temp_df = temp_df.sort_values(by=["ScanDate", "Scan"]) 

    firstFrac = temp_df.ScanDate.min()

    temp_df["DaysfromFrac1"] = temp_df["ScanDate"] - firstFrac
    temp_df['DaysfromFrac1'] = temp_df['DaysfromFrac1'].dt.days.astype('int16')
    
    print(temp_df)

    sns.scatterplot(x="DaysfromFrac1", y="Mean", hue="Observer", style="Region", palette=colourmap,data=temp_df, x_jitter=100)
    plt.ylim(0,max_signal+5)


    #plt.xticks("Scan",Timepoints, rotation=45)
    plt.legend(loc="upper right")
    fig.savefig(output + str(i) + ".png", dpi=300)
    print("-------------------------------------")

