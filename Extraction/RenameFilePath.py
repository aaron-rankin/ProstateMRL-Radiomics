import os

url = "D:\\prostateMR_radiomics\\patientData\\SABR_new\\"

ptDir = os.listdir(url)

for i in ptDir:
    scanWeeks = os.listdir(url + str(i))

    for j in scanWeeks:
        files = os.listdir(url + str(i) + "\\" + str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        for k in files:
            if "Adm" in k:
                print("Before: " + k)
                Admfolder = "D:\\prostateMR_radiomics\\AdmireContours\\SABR_new\\" + i + "\\"
                if os.path.exists(Admfolder):
                    print()
                else:
                    os.mkdir(Admfolder)

                os.rename(url + str(i) + "\\" + str(j) + "\\" + str(k), Admfolder + "\\" + str(i) + str(j) +"AdmCont.dcm")
                print("-----------------")
                