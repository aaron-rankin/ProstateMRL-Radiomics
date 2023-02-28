from LongitudinalModel import LongitudinalModel as LM
from DeltaModel import DeltaModel as DM
from Functions import UsefulFunctions as UF

DataRoot = UF.DataRoot(1)
Norm = "HM-FSTP"
Extract = "No"

LM(DataRoot, Norm, Extract)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
DM(DataRoot, Norm)



