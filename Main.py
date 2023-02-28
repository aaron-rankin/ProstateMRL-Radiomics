from LongitudinalModel import LongitudinalModel as LM
from DeltaModel import DeltaModel as DM
from Functions import UsefulFunctions as UF
import pandas as pd

DataRoot = UF.DataRoot(2)
Norm = "HM-FS"
Extract = "No"

def ModelSummary(root, Norm):
    dir = root + "Aaron\ProstateMRL\Data\Paper1\\" + Norm + "\\Features\\"

    print("Model Summary - " + Norm)
    print("")
    print("-------------------------")
    print("ICC Reduction")
    print("Features Before: 105")

    L_ICC = pd.read_csv(dir + "Longitudinal_FeaturesRemoved_ICC.csv")
    L_ICC_fts = len(L_ICC["Feature"].unique())
    print("Longitudinal Features Removed: " + str(L_ICC_fts))
    print("")
    D_ICC = pd.read_csv(dir + "Delta_FeaturesRemoved_ICC.csv")
    D_ICC_fts = len(D_ICC["Feature"].unique())
    print("Delta Features Removed: " + str(D_ICC_fts))

    print("-------------------------")
    print("Volume Reduction")
    print("")
    print("Longitudinal Features Before: " + str(105 - L_ICC_fts))
    L_Vol = pd.read_csv(dir + "Longitudinal_FeaturesRemoved_Volume.csv")
    L_Vol_fts = len(L_Vol["Feature"].unique())
    print("Longitudinal Features Removed: " + str(L_Vol_fts))

    print("")
    print("Delta Features Before: " + str(105 - D_ICC_fts))
    D_Vol = pd.read_csv(dir + "Delta_FeaturesRemoved_Volume.csv")
    D_Vol_fts = len(D_Vol["Feature"].unique())
    print("Delta Features Removed: " + str(D_Vol_fts))

    print("-------------------------")
    print("Feature Selection")
    print("")
    print("Longitudinal Features Before: " + str(105 - L_ICC_fts - L_Vol_fts))
    L_Select = pd.read_csv(dir + "Longitudinal_SelectedFeatures.csv")
    L_Select_fts = L_Select["Feature"].unique()
    print("Longitudinal Features Selected: " + str(len(L_Select_fts)))

    print("")
    print("Delta Features Before: " + str(105 - D_ICC_fts - D_Vol_fts))
    D_Select = pd.read_csv(dir + "Delta_SelectedFeatures.csv")
    D_Select_fts = D_Select["Feature"].unique()
    print("Delta Features Selected: " + str(len(D_Select_fts)))

    # check if any features are selected in both longitudinal and delta
    print("")
    print("Features Selected in Both Longitudinal and Delta: " + str(len(set(L_Select_fts) & set(D_Select_fts))))

    print("-------------------------")

LM(DataRoot, Norm, Extract, 1.25)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
DM(DataRoot, Norm)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
ModelSummary(DataRoot, Norm)


