import os

url = "D:\\data\\prostateMR_radiomics\\patientData\\20fractions_new\\"

ptDir = os.listdir(url)

for i in ptDir:
    scanWeeks = os.listdir(url + str(i))

    for j in scanWeeks:
        files = os.listdir(url + str(i) + "\\" + str(j))
        print ("Processing: "+i+"  Timepoint: "+j)	
        for k in files:
            if "Admire" in k:
                os.rename(url + str(i) + "\\" + str(j) + "\\" + str(k), url + str(i) + "\\" + str(j) + "\\" + "AdmireContour"+ str(i)+str(j)+".dcm")