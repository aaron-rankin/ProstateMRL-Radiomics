import os

url = "D:\\prostateMR_radiomics\\nifti_new\\new_SABR\\"

ptDir = os.listdir(url)

for i in ptDir:
    scanWeeks = os.listdir(url + str(i))

    for j in scanWeeks:
        files = os.listdir(url + str(i) + "\\" + str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        for k in files:
            if "RP" in k:
                print("Before: " + k)
                os.rename(url + str(i) + "\\" + str(j) + "\\" + str(k), url + str(i) + "\\" + str(j) + "\\" + str(i) + "_" + str(j)+ "_RP_Prostate.nii")
                print("-----------------")
                