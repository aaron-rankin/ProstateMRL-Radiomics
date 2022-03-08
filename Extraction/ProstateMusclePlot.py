"""""

Aaron Rankin 08/03/22
Reads in csv with mean and std of MR signal from prostate contours and msucle clicks
Plots values

"""""

from cProfile import label
import string
from turtle import title
from wsgiref.simple_server import sys_version
import SimpleITK as sitk
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys
import pandas as pd

# load in csv -- Change according to dataset
url = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions.csv"

# output directories for plots
out_20f = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions\\"
out_20f_new = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\20fractions_new\\"
out_SABR = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR\\"
out_SABR_new = "D:\\data\\Aaron\\ProstateMRL\\Data\\Extraction\\Mean_values\\Raw\\SABR_new\\"

output = out_20f

df = pd.read_csv(url)

plt.figure("Mean Intensity Plot")
plt.title("Mean Signal Intensity Patient: " + i)
plt.ylabel("MR Intensity")
plt.xlabel("MR Scan")

groupedObs = df.groupby("Observer")
for name, group in groupedObs:
    fig = plt.plot(groupedObs["Scan"], groupedObs["Mean Prostate"], marker="o", linestyle="", label = name)
plt.legend
fig.savefig(output + str(i) + ".png", dpi = 300)
plt.clf

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