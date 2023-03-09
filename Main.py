from LongitudinalModel import LongitudinalModel as LM
from DeltaModel import DeltaModel as DM
from Functions import UsefulFunctions as UF
import pandas as pd

DataRoot = UF.DataRoot(2)
#Norm = "HM-FS"
Extract = "No"

def ModelSummary(root, Norm):
    dir = root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\"
    out = open(root + "Aaron\ProstateMRL\Data\Paper1\\NormSummary\\" + Norm + "2.txt", "w")

    out.write("Model Summary - " + Norm)
    out.write("\n")
    out.write("-------------------------\n")
    out.write("ICC Reduction\n")
    out.write("Features Before: 105\n")

    L_ICC = pd.read_csv(dir + "Longitudinal_FeaturesRemoved_ICC.csv")
    L_ICC_fts = len(L_ICC["Feature"].unique())
    out.write("Longitudinal Features Removed: " + str(L_ICC_fts) + "\n")
    out.write("\n")
    D_ICC = pd.read_csv(dir + "Delta_FeaturesRemoved_ICC.csv")
    D_ICC_fts = len(D_ICC["Feature"].unique())
    out.write("Delta Features Removed: " + str(D_ICC_fts) + "\n")

    out.write("-------------------------\n")
    out.write("Volume Reduction\n")
    out.write("\n")
    out.write("Longitudinal Features Before: " + str(105 - L_ICC_fts) + "\n")
    L_Vol = pd.read_csv(dir + "Longitudinal_FeaturesRemoved_Volume.csv")
    L_Vol_fts = len(L_Vol["Feature"].unique())
    out.write("Longitudinal Features Removed: " + str(L_Vol_fts)+ "\n")

    out.write("\n")
    out.write("Delta Features Before: " + str(105 - D_ICC_fts)+ "\n")
    D_Vol = pd.read_csv(dir + "Delta_FeaturesRemoved_Volume.csv")
    D_Vol_fts = len(D_Vol["Feature"].unique())
    out.write("Delta Features Removed: " + str(D_Vol_fts) + "\n")

    out.write("-------------------------\n")
    out.write("Feature Selection\n")
    out.write("\n")
    out.write("Longitudinal Features Before: " + str(105 - L_ICC_fts - L_Vol_fts) + "\n")
    L_Select = pd.read_csv(dir + "Longitudinal_SelectedFeatures.csv")
    L_Select_fts = L_Select["Feature"].unique()
    out.write("Longitudinal Features Selected: " + str(len(L_Select_fts)) + "\n")

    out.write("\n")
    out.write("Delta Features Before: " + str(105 - D_ICC_fts - D_Vol_fts)+ "\n")
    D_Select = pd.read_csv(dir + "Delta_SelectedFeatures.csv")
    D_Select_fts = D_Select["Feature"].unique()
    out.write("Delta Features Selected: " + str(len(D_Select_fts))+ "\n")

    # check if any features are selected in both longitudinal and delta
    out.write("\n")
    out.write("Features Selected in Both Longitudinal and Delta: " + str(len(set(L_Select_fts) & set(D_Select_fts)))+ "\n")

    out.write("-------------------------\n")
Norms = ["Raw", "HM-FS", "HM-TP", "HM-FSTP", "Med-Pros", "Med-Psoas"]
#n= "HM-FS"
for n in Norms:
    LM(DataRoot, n, Extract, 1.5, output=False)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    DM(DataRoot, n, output=False)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    ModelSummary(DataRoot, n)
    # read in model summary
    #f = open(DataRoot + "Aaron\ProstateMRL\Data\Paper1\\NormSummary\\" + n + ".txt", "r")
    #print(f.read())



