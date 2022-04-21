"""""

Aaron Rankin 08/03/22
Reads in csv with mean and std of MR signal from prostate contours and msucle clicks
Plots values

"""""

import enum
from random import randint
import numpy as np
import pandas as pd
from scipy import rand
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
# load in csv -- Change according to dataset
url = "D:\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\Datafiles\\SABR_new.csv"

# output directories for plots
out_20f = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\HM1\\20fractions\\"
out_20f_new = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions_new\\"
out_SABR = "D:\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR\\"
out_SABR_new = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR_new\\"

output = out_SABR_new

df = pd.read_csv(url)

patIDs = df.PatID.unique()
print(patIDs)

Obs = df.Observer.unique()
rgb_vals = sns.color_palette("colorblind", len(Obs))
colourmap = dict(zip(Obs, rgb_vals))

max_signal = 140

for i in patIDs:
    print("Processing patient: " + str(i))

    fig = plt.figure(figsize=(10,7))
    sns.set(style="darkgrid")
    plt.title("Mean MR signal (Raw) - Patient: " + str(i), fontsize=20)
    plt.xlabel("Days from Fraction 1")
    plt.ylabel("Mean Signal")
    plt.ylim(0,max_signal+5)

    plt.xlim(-1, 16)
    plt.xticks(np.arange(0,16,2))

    temp_df = df[df["PatID"].isin([i])]
    temp_df["ScanDate"] = pd.to_datetime(temp_df["ScanDate"], dayfirst=True) 
    temp_df = temp_df.sort_values(by=["ScanDate", "Scan"]) 

    firstFrac = temp_df.ScanDate.min()

    temp_df["DaysfromFrac1"] = temp_df["ScanDate"] - firstFrac
    temp_df['DaysfromFrac1'] = temp_df['DaysfromFrac1'].dt.days.astype('int16')
    
    print(temp_df)

    plot1 = sns.scatterplot(x="DaysfromFrac1", y="Mean", hue="Observer", style="Region", palette=colourmap,data=temp_df, x_jitter=100)

    box = plot1.get_position()
    plot1.set_position([box.x0, box.y0, box.width * 0.85, box.height]) # resize position

# Put a legend to the right side
    plot1.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), ncol=1)
    #fig.savefig(output + str(i) + ".png", dpi=300)
    print("-------------------------------------")

