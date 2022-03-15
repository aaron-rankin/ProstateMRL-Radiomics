import os

url = "D:\\data\\prostateMR_radiomics\\nifti\\20fractions\\"
url_clicks  = "D:\\data\\prostateMR_radiomics\\MuscleClicks\\20fractions\\"
ptDir = os.listdir(url)
clDir = os.listdir(url_clicks)
"""""
for i in ptDir:
    scanWeeks = os.listdir(url + str(i))
    print(i)
    for j in scanWeeks:
        files = os.listdir(url + str(i) + "\\" + str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        for k in files:
                os.rename(url_clicks + str(i) + "_" + str(j) + ".nii", url + str(i) + "\\" + str(j) + "\\" + str(i) + "_" + str(j) + "_muscle.nii")
                print("-----------------")
"""

for k in clDir:
    print(k)
    name = k.split("_")
    patID = name[0]
    scan = name[1]
    scan = scan[:-4]
    print(scan)    
    os.rename(url_clicks + str(k), url + patID + "\\" + scan + "\\" + patID + "_" + scan + "_muscle.nii")