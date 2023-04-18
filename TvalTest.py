from Functions import UsefulFunctions as UF
from Functions import VisualisationFunctions as VF
from Clustering import Clustering as Cl
import numpy as np

####################################################

DataRoot = UF.DataRoot(1)
Norm = "HM-FS"
Extract = "No"
output = False 
t_vals = np.arange(1, 3.01, 0.25)

for t_val in t_vals:
    tag = "Testt_" + str(t_val) # if using Filters, specify "Filters_" in tag

    ####################################################

    Cl.LongitudinalModel(DataRoot, Norm, Extract, t_val, tag, output)
    #Dl.DeltaModel(DataRoot, Norm, tag, output)
    UF.ModelSummary(DataRoot, Norm, tag)
