import os

url = "D:\\data\\prostateMR_radiomics\\nifti\\SABR_new\\"
url_clicks  = "D:\data\prostateMR_radiomics\MuscleClicks\paint_SABR_new_glute\\"
ptDir = os.listdir(url)
clDir = os.listdir(url_clicks)

'''
for i in ptDir:
    scanWeeks = os.listdir(url + str(i))
    print(i)
    for j in scanWeeks:
        files = os.listdir(url + str(i) + "\\" + str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        for k in files:
            if "muscle" in k:
                print(k)
                os.rename(url + str(i) + "\\" + str(j) + "\\" + str(i) + "_" + str(j) +"_muscle.nii", url + str(i) + "\\" + str(j) + "\\" + str(i) + "_" + str(j) + "_glute.nii")
                print("-----------------")

'''
for k in clDir:
    print(k)
    name = k.split("_")
    patID = name[2]
    scan = name[3]
    scan = scan[:-4]
    print(patID)
    print(scan)    
    os.rename(url_clicks + str(k), url + patID + "\\" + scan + "\\" + patID + "_" + scan + "_glute.nii")
