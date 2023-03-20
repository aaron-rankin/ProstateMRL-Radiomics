from LongitudinalModel import LongitudinalModel as LM
from DeltaModel import DeltaModel as DM
from Functions import UsefulFunctions as UF
import pandas as pd

DataRoot = UF.DataRoot(2)
#Norm = "HM-FS"
Extract = "Yes"


#Norms = ["Raw", "HM-FS", "HM-TP", "HM-FSTP", "Med-Pros", "Med-Psoas"]
n= "HM-FS"
#for n in Norms:
LM(DataRoot, n, Extract, 2, output=True)
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#DM(DataRoot, n, output=False)
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#ModelSummary(DataRoot, n)
    # read in model summary
    #f = open(DataRoot + "Aaron\ProstateMRL\Data\Paper1\\NormSummary\\" + n + ".txt", "r")
    #print(f.read())



