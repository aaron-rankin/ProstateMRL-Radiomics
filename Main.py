from Functions import UsefulFunctions as UF
from Functions import VisualisationFunctions as VF
from Clustering import Clustering as Cl
from Delta import Delta as Dl

####################################################

DataRoot = UF.DataRoot(1)
Norm = "Med-Glute"
Extract = "No"
tag = "Baseline" # if using Filters, specify "Filters_" in tag
output = False 
t_val = 2

####################################################

#Cl.LongitudinalModel(DataRoot, Norm, Extract, t_val, tag, output)
Dl.DeltaModel(DataRoot, Norm, tag, output)
UF.ModelSummary(DataRoot, Norm, tag)

####################################################

#VF.MedianSignalPlot(DataRoot, Norm)
#VF.ClusterSignalPlots(DataRoot, Norm, tag)
#VF.SelectedFeatures(DataRoot, Norm, tag, "Longitudinal")