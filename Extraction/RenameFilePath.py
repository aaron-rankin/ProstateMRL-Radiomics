import os

url = "D:\\data\\prostateMR_radiomics\\nifti\\20fractions\\"
url_clicks  = "D:\data\prostateMR_radiomics\MuscleClicks\paint_SABR_new_glute\\"
ptDir = os.listdir(url)
clDir = os.listdir(url_clicks)

folders = ["BaseImages", "Masks", "Reg-Raw", "Norm-Pros","Norm-Glute", "Norm-Psoas", "HM-TP", "HM-FS"]
del_folders = ["Norm-Images", "HM-Images", "HM-Scan1"]

'''
for i in ptDir:
    scanWeeks = os.listdir(url + str(i))
    for j in scanWeeks:
       # files = os.listdir(url + str(i) + "\\" + str(j) + "\\Norm-Images\\")

        print("Processing: "+i+"  Timepoint: "+j)
        print("-----------------")
        
        path = url + str(i) + "\\" + str(j) + "\\"

        for folder in folders:
            if os.path.exists(path + folder):
                continue
            else:
                os.mkdir(path + folder)
        for del_folder in del_folders:
            if os.path.exists(path + del_folder):
                os.rmdir(path + del_folder)
            else:
                continue


        for k in files:
           
            if "Glute" in k:
                os.rename(path + "Norm-Images\\"+str(k), path + "Norm-Glute\\" + str(k)) 

            if "Psoas" in k:
                os.rename(path + "Norm-Images\\"+str(k), path + "Norm-Psoas\\" + str(k))        

            if "Pros" in k:
                os.rename(path + "Norm-Images\\"+str(k), path + "Norm-Pros\\" + str(k)) 



        for k in files:
            if os.path.isdir(path + str(k)):
                continue
            elif "image" in k:
                os.rename(path + str(k),path + "BaseImages" + "\\" + str(k))
            elif "reg" in k:
                os.rename(path + str(k),path + "Reg-Raw" + "\\" + str(k)[3:])
            elif "Prostate" in k:
                os.rename(path + str(k), path + "Masks" + "\\" + str(i) + "_" + str(k))
            elif "glute" or "psoas" or "body_mask" or "shrunk" in k:
                os.rename(path + str(k), path + "Masks" + "\\" + str(k))


            #os.mkdir(path + "test")
        #	
            #for k in files:
             # print(k)

           # if "shrunk" in k:
           # print(url + str(i) + "\\" + str(j) + "\\" + str(k))
        #        name = str(k)
         #       print(name)
          #      new_name = "000" + name
           #     print(new_name)
                #os.rename(url + str(i) + "\\" + str(j) + "\\" + str(k), url + str(i) + "\\" + str(j) + "\\" + "000" + str(k))
            

'''

for k in ptDir:
    if "glute" in k:
        print(k)
        name = k.split("_")
        group = name[0] #+ #"_" + name[1]
        patID = name[1]
        scan = name[2]
        scan = scan[:-4]
        # print(group)
        # print(patID)
        # print(scan)    
        print(url + group + "\\" + patID + "\\" + scan + "\\" + patID + "_" + scan + "_glute2.nii")
        os.rename(url + "\\" + patID + "\\" + scan + "\\" + patID + "_" + scan + "_glute2.nii", url + "\\" + patID + "\\" + scan + "\\Masks\\" + patID + "_" + scan + "_glute2.nii")

