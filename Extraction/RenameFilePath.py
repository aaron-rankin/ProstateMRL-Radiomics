import os

url = "D:\\data\\prostateMR_radiomics\\nifti\\SABR\\"
url_clicks  = "D:\\data\\prostateMR_radiomics\\MuscleClicks\\SABR\\"
ptDir = os.listdir(url)
clDir = os.listdir(url_clicks)


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
    print(k)
    name = k.split("_")
    patID = name[1]
    scan = name[2]
    scan = scan[:-4]
    print(patID)
    print(scan)    
    os.rename(url_clicks + str(k), url + patID + "\\" + scan + "\\" + patID + "_" + scan + "_muscle.nii")
'''