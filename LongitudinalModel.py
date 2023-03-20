
from Features import Extraction as FE
from Features import Reduction as FR
import Functions as Fn
from Functions import UsefulFunctions as UF
from Clustering import Clustering as Cl

# DataRoot = UF.DataRoot(1) # 1 if server / 2 if local
# Norm = "HM-FS"
# Extract = "Yes"

def LongitudinalModel(DataRoot, Norm, Extract, t_val, output=False):# Make Directories if they don't exist
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
    if output == True:
        print("------------------------------------")
        print("------------------------------------")
        print("Reducing Features...")
        print("Volume Correlation Feature Reduction: ")
        print("------------------------------------")
        print("------------------------------------")

    #FR.Volume(DataRoot, Norm, "Longitudinal", output)
    if output == True:
        print("------------------------------------")
        print("ICC Feature Reduction: ")
        print("------------------------------------\n ")
    #FR.ICC(DataRoot, Norm, "Longitudinal", output)
    # Clustering
    if output == True:
        print("------------------------------------")
        print("------------------------------------")
        print("Clustering...")
        print("------------------------------------")
        print("Creating Distance Matrices: ")
        print("------------------------------------")
    #Cl.DistanceMatrix(DataRoot, Norm, output)
    
    if output == True:
        print("------------------------------------")
        print("Clustering Distance Matrices: ")
        print("------------------------------------")
    Cl.ClusterFeatures(DataRoot, Norm, t_val, output)
    Cl.ClusterCount(DataRoot, Norm, output)
    if output == True:
        print("Feature Selection: ")
        print("------------------------------------")
    Cl.ClusterSelection(DataRoot, Norm, output)
    print("------------------------------------")
    print("------------------------------------\n ")




