import sys
import os


current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to
# the sys.path.
sys.path.append(parent + "\\Functions\\")

import UsefulFunctions as UF
import ImageFunctions as IF

print(UF.SABRPats())

print(IF.MaskValue("pros"))