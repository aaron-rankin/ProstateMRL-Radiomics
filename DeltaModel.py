from Features import Extraction as FE
from Features import Reduction as FR
from Functions import UsefulFunctions as UF
from Delta import Delta as DL
# DataRoot = UF.DataRoot(1)
# Norm = "Raw"

def DeltaModel(DataRoot, Norm, output=False):
    # Make Directories if they don't exist
    print("------------------------------------")
    print("------------------------------------")
    print("Root: {} Norm: {}".format(DataRoot, Norm))
    UF.CD(DataRoot, Norm)

    # Get Delta Features
    if output == True:
        print("------------------------------------")
        print("------------------------------------")
        print("Calculating Delta Features...")
        print("------------------------------------")
    FE.DeltaValues(DataRoot, Norm)

    # Feature Reduction
    if output == True:
        print("------------------------------------")
        print("------------------------------------")
        print("Reducing Features...")
        print("------------------------------------")
        print("ICC Feature Reduction: ")
        print("------------------------------------")
    FR.ICC(DataRoot, Norm, "Delta", output)
    FR.Volume(DataRoot, Norm, "Delta", output)
    if output == True:
        print("------------------------------------")
        print("------------------------------------\n ")
        print("------------------------------------")
        print("------------------------------------")
        print("Feature Selection...")
        print("------------------------------------")
        print("Creating Correlation Matrix:")
        print("------------------------------------")
    DL.CorrMatrix(DataRoot, Norm)
    if output == True:
        print("------------------------------------")
        print("Feature Selection:")
        print("------------------------------------")
    DL.FeatureSelection(DataRoot, Norm, output)
    print("------------------------------------")
    print("------------------------------------\n ")