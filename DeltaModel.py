from Features import Extraction as FE
from Features import Reduction as FR
from Functions import UsefulFunctions as UF
from Delta import Delta as DL
# DataRoot = UF.DataRoot(1)
# Norm = "Raw"

def DeltaModel(DataRoot, Norm):
    # Make Directories if they don't exist
    print("------------------------------------")
    print("------------------------------------")
    print("Checking Directories...")
    print("Root: {} Norm: {}".format(DataRoot, Norm))
    UF.CD(DataRoot, Norm)
    print("------------------------------------")
    print("------------------------------------\n ")

    # Get Delta Features
    print("------------------------------------")
    print("------------------------------------")
    print("Calculating Delta Features...")
    print("------------------------------------")
    FE.DeltaValues(DataRoot, Norm)
    print("------------------------------------")
    print("------------------------------------\n ")

    # Feature Reduction
    print("------------------------------------")
    print("------------------------------------")
    print("Reducing Features...")
    print("------------------------------------")
    print("ICC Feature Reduction: ")
    print("------------------------------------")
    FR.ICC(DataRoot, Norm, "Delta")
    print("------------------------------------")
    print("Volume Correlation Feature Reduction: ")
    print("------------------------------------")
    FR.Volume(DataRoot, Norm, "Delta")
    print("------------------------------------")
    print("------------------------------------\n ")

    # Feature Selection
    print("------------------------------------")
    print("------------------------------------")
    print("Feature Selection...")
    print("------------------------------------")
    print("Creating Correlation Matrix:")
    print("------------------------------------")
    DL.CorrMatrix(DataRoot, Norm)
    print("------------------------------------")
    print("------------------------------------")
    print("Feature Selection:")
    print("------------------------------------")
    DL.FeatureSelection(DataRoot, Norm)
    print("------------------------------------")
    print("------------------------------------\n ")