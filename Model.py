import SimpleITK as sitk
import numpy as np
import pandas as pd
import os
from datetime import datetime
import radiomics
from radiomics import featureextractor
import sys
from tqdm import tqdm
from Functions import UsefulFunctions as UF
from Functions import CreateDirs as CD
from Features import Extraction as Ex
from Features import Reduction as Rd
from Clustering import Clustering as CM

print(UF.SABRPats())

root = UF.DataRoot(2)
Norm = "HM-FSTP"

print("-" * 10)
CD.CreateDirs(root, "Test")
print("-" * 10)

#print(Ex.All(root, Norm)[1])
print("-" * 10)
#print(Ex.Limbus(root, Norm)[1])
print("-" * 10)

Rd.ICC(root, Norm)

Rd.Volume(root, Norm)

CM.Model(root, Norm, 1.5)