from Functions import UsefulFunctions as UF
from Functions import VisualisationFunctions as VF
from Clustering import Clustering as Cl
from Delta import Delta as Dl

####################################################

DataRoot = UF.DataRoot(2)
Norm = "HM-FS"
Extract = "No"
tag = "t_val_15" # if using Filters, specify "Filters_" in tag
output = False 
t_val = 1.5

####################################################

Cl.LongitudinalModel(DataRoot, Norm, Extract, t_val, tag, output)
Dl.DeltaModel(DataRoot, Norm, tag, output)
UF.ModelSummary(DataRoot, Norm, tag)

####################################################

#VF.MedianSignalPlot(DataRoot, Norm)
#VF.ClusterSignalPlots(DataRoot, Norm, tag)
#VF.SelectedFeatures(DataRoot, Norm, tag, "Longitudinal")