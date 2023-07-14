from fileinput import filelineno
import os
from tqdm import tqdm
nifti_dir = "D:\\data\\prostateMR_radiomics\\nifti\\"

ts = os.listdir(nifti_dir)

for t in ts:
    t_dir = os.path.join(nifti_dir, t)

    pats = os.listdir(t_dir)

    for pat in tqdm(pats):
        p_dir = os.path.join(t_dir, pat)

        scans = os.listdir(p_dir)

        for scan in scans:
            s_dir = os.path.join(p_dir, scan)

            image_roots = ["Raw\\", "HM-TP\\", "HM-FS\\", "HM-FSTP\\","Mean-Pros\\", "Mean-Glute\\", "Mean-Psoas\\", "Med-Pros\\", "Med-Glute\\", "Med-Psoas\\", "Masks\\"]
            # make list of roots joined with scan path
            image_roots = [os.path.join(s_dir, root) for root in image_roots]
            #image_paths = 
            folders = os.listdir(s_dir)

            # remove unnessesary folders
            #print(folders)
            for folder in folders:
                f_dir = os.path.join(s_dir, folder + "\\")
                if (f_dir) not in image_roots:
                    #print(folder)
                    continue
                if folder == "Raw":
                    files = os.listdir(f_dir)
                    for file in files:
                        if "HM" in file:
                            #print(file)
                            os.remove(f_dir + file)
                    