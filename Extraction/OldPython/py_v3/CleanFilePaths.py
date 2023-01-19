import os

from importlib_resources import path
import UsefulFunctions as UF
#root = UF.DataRoot()

root = "D:\\data\\"
url = root + "prostateMR_radiomics\\nifti\\" 

t_dir = os.listdir(url)

folders = ["RawImages", "Masks", "HM-TP", "HM-FS", "HM-FSTP","Norm-Pros", "Norm-Glute", "Norm-Psoas", "Med-Pros", "Med-Psoas", "Med-Glute", "Z-Score", "WS", "OldImages"]

for t in t_dir: 
    p_dir = os.listdir(os.path.join(url, t))
    print(p_dir)

    for p in p_dir:
        sc_dir = os.listdir(os.path.join(url, t, p))

        for s in sc_dir:
            pat_path = os.path.join(url, t, p, s)
    
            '''
            Make folders
            '''
            # # if os.path.exists(pat_path + "\\BaseImagesReg"):
            # #     os.rmdir(pat_path + "\\BaseImagesReg")
            # for f in folders:
            #     norm_path = os.path.join(pat_path, f)

            #     if os.path.exists(norm_path):
            #         continue

            #     else:
                    #os.mkdir(norm_path) 
                      
            '''
            Clean up folders (for _new patients)
            '''
            
            # files = os.listdir(pat_path)
            # for f in files: 
            #     file_path = os.path.join(pat_path, f)
            #     if os.path.isfile(file_path) == True:
            #         #print(file_path)

            #         if "ostate" in f:
            #             os.rename(file_path, (os.path.join(pat_path, "Masks",f)))
                    
            #         elif "psoas" in f:
            #              os.rename(file_path, (os.path.join(pat_path, "Masks",f)))
                    
            #         elif "glute" in f:
            #              os.rename(file_path, (os.path.join(pat_path, "Masks",f)))

            #         elif "body" in f:
            #              os.rename(file_path, (os.path.join(pat_path, "Masks",f)))
                        
            #         elif "HM" in  f:
            #              os.rename(file_path, (os.path.join(pat_path, "OldImages",f)))

            #         elif "NORM" in f:
            #              os.rename(file_path, (os.path.join(pat_path, "OldImages",f)))

            #         elif p + "_" + s + "_image.nii" == f:
            #              os.rename(file_path, (os.path.join(pat_path, "BaseImages",f)))

            #         else:
            #             print(f)
            '''
            Change to Raw from image
            '''
            # raw_path = os.path.join(pat_path, "RawImages")
            # files = os.listdir(raw_path)
            # for f in files: 
            #     if f == p + "_" + s + "_image.nii":
            #         old_name = os.path.join(raw_path, f)
            #         new_name = os.path.join(raw_path, (p + "_" + s + "_Raw.nii"))
            #         os.rename(old_name, new_name)
            mask_path = os.path.join(pat_path, "Masks")
            files = os.listdir(mask_path)
            for f in files: 
                #print(f)
                if f == p +"_"+ s  + "_RP_Prostate" + ".nii":
                    print(f)
                    old_name = os.path.join(mask_path, f)
                    new_name = os.path.join(mask_path, (p + "_" + s + "_Prostate_RP.nii"))
                    os.rename(old_name, new_name)