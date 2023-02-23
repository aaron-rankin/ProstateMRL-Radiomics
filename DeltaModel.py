from Features import Extraction as FE
from Features import Reduction as FR
import Functions as Fn
from Functions import UsefulFunctions as UF
from Clustering import Clustering as Cl

DataRoot = UF.DataRoot(2)
Norm = "HM-FSTP"
Extract = "No"

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

