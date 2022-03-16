from pyXDR import pyXDR
#from pyXDR.pyXDR import XDRImage as XDRImage

image = pyXDR.read("D://prostateMR_radiomics//MuscleClicks//test.xdr")

print(image.data)
