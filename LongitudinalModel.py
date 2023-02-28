
from Features import Extraction as FE
from Features import Reduction as FR
import Functions as Fn
from Functions import UsefulFunctions as UF
from Clustering import Clustering as Cl

# DataRoot = UF.DataRoot(1) # 1 if server / 2 if local
# Norm = "HM-FS"
# Extract = "Yes"

def LongitudinalModel(DataRoot, Norm, Extract, t_val):# Make Directories if they don't exist
    print("------------------------------------")
    print("------------------------------------")
    # print("Checking Directories...")
    print("Root: {} Norm: {}".format(DataRoot, Norm))
    UF.CD(DataRoot, Norm)
    # print("------------------------------------")
    # print("------------------------------------\n ")


    # Extract Features
    if Extract == "Yes":
        print("------------------------------------")
        print("------------------------------------")
        print("Extracting Features...")
        FE.All(DataRoot, Norm)
        print("Extracted - All")
        print("------------------------------------")
        FE.Limbus(DataRoot, Norm)
        print("Extracted - Limbus")
        print("------------------------------------")
        print("------------------------------------\n ")

    # Feature Reduction
    print("------------------------------------")
    print("------------------------------------")
    print("Reducing Features...")
    print("------------------------------------")
    print("ICC Feature Reduction: ")
    print("------------------------------------")

    FR.ICC(DataRoot, Norm, "Longitudinal")
    print("------------------------------------")
    print("Volume Correlation Feature Reduction: ")
    print("------------------------------------")

    FR.Volume(DataRoot, Norm, "Longitudinal")
    print("------------------------------------")
    print("------------------------------------\n ")

    # Clustering
    print("------------------------------------")
    print("------------------------------------")
    print("Clustering...")
    print("------------------------------------")
    print("Creating Distance Matrices: ")
    print("------------------------------------")
    Cl.DistanceMatrix(DataRoot, Norm)
    print("------------------------------------")
    print("Clustering Distance Matrices: ")
    print("------------------------------------")
    Cl.ClusterFeatures(DataRoot, Norm, t_val)
    print("------------------------------------")
    Cl.ClusterCount(DataRoot, Norm)
    print("Feature Selection: ")
    print("------------------------------------")
    Cl.ClusterSelection(DataRoot, Norm)
    print("------------------------------------")
    print("------------------------------------\n ")




