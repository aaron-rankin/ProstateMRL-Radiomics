"""""

Aaron Rankin 21/04/22
Reads in csv for packcomp, plots signal change against time at each fraction

"""""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

df = pd.read_csv('D:/data/Aaron/ProstateMRL/Data/MRLPacks/MeanValues/0001088.csv')
output = 'D:/data/Aaron/ProstateMRL/Data/MRLPacks/RawPlots/0001088'

fractions = df.Fraction.unique()
rgb_vals = sns.color_palette("colorblind", len(fractions))
colourmap = dict(zip(fractions, rgb_vals))

fig = plt.figure(figsize=(10,7))
sns.set_theme(style='darkgrid')
plt.title("Mean MR signal Change (Raw) - Patient:0001088", fontsize=20)
plt.xlabel("Time Change from Scan 1 (mins)")   
plt.ylabel("Mean Signal Change")
plt.ylim(-120,270)

#print("Converting Time")
df["TimeDiff"] = df["TimeDiff"].apply(lambda x: x[-8:-3])
df["TimeDiff"].replace([""], "0", inplace=True)
temp = pd.DataFrame()
for index, row in df.iterrows():
    newtime = {"TotalMins":[]}
    hours = int(row["TimeDiff"][0:2])
    if len(row["TimeDiff"]) > 1: 
        mins = int(row["TimeDiff"][3:5])
    else:
        mins = 0
    total_mins = hours*60 + mins
    newtime["TotalMins"] = total_mins
    temp = temp.append(newtime, ignore_index=True)

region = "Prostate"

df = pd.concat([df,temp],axis=1)
df_pros = df.loc[df["Region"].isin([region])]
plt.title("Mean MR signal Change (Raw) - Patient: 0001088 - " + region, fontsize=20)
plot_pros = sns.scatterplot(data=df_pros, x='TotalMins', y='SignalChange', hue='Fraction', palette=colourmap)
box = plot_pros.get_position()
plot_pros.set_position([box.x0, box.y0, box.width * 0.85, box.height]) # resize position

# Put a legend to the right side
plot_pros.legend(loc='center right', bbox_to_anchor=(1.25, 0.5), ncol=1, title="Fraction")
fig.savefig(output+ "_" + region + ".png", dpi=300)    
print("-------------------------------------")
    
