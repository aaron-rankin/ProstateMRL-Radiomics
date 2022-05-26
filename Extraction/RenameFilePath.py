import os

url = "D:\\data\\prostateMR_radiomics\\nifti\\"
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
            if "shrunk" in k:
                print(url + str(i) + "\\" + str(j) + "\\" + str(k))
                name = str(k)
                print(name)
                new_name = "000" + name
                print(new_name)
                os.rename(url + str(i) + "\\" + str(j) + "\\" + str(k), url + str(i) + "\\" + str(j) + "\\" + "000" + str(k))
                print("-----------------")

'''

for k in clDir:
    if "new" not in k:
        print(k)
        name = k.split("_")
        group = name[0] #+ #"_" + name[1]
        patID = name[1]
        scan = name[2]
        scan = scan[:-4]
        # print(group)
        # print(patID)
        # print(scan)    
        print(url + group + "\\" + patID + "\\" + scan + "\\" + patID + "_" + scan + "_psoas.nii")
        os.rename(url_clicks + str(k), url + group + "\\" + patID + "\\" + scan + "\\" + patID + "_" + scan + "_psoas.nii")
