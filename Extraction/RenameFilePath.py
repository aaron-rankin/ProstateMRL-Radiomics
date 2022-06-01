import os

url = "D:\\data\\prostateMR_radiomics\\nifti\\SABR\\"
url_clicks  = "D:\data\prostateMR_radiomics\MuscleClicks\paint_SABR_new_glute\\"
ptDir = os.listdir(url)
clDir = os.listdir(url_clicks)

folders = ["BaseImages", "Masks", "Reg-Raw", "Norm-Pros","Norm-Glute", "Norm-Psoas", "HM-TP", "HM-Scan1"]
del_folders = ["Norm-Images", "HM-Images"]


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

'''
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

'''