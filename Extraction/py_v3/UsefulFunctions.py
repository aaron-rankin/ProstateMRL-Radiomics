import SimpleITK as sitk
import numpy as np
import numpy.ma as ma
from matplotlib import pyplot
import matplotlib.pyplot as plt
import os
import sys
import seaborn as sns
import pandas as pd
from datetime import datetime

####################################################

def DataRoot():
    '''
    Returns the root directory of the data if on
    server or local
    '''
    question = input("Server (1) or Local (2)? ")
    if question == str(1):
        root = "D:\\data\\"
    elif question == str(2):
        root = "\\\\130.88.233.166\\data\\"
    
    return root

#####################################################

def NormArray():
    """
    Returns array of normalisation factors
    """
    Norms = ["Raw", "HM-FS", "HM-TP", "Norm-Pros", "Med-Pros", "Norm-Glute", "Med-Glute", "Norm-Psoas", "Med-Psoas"]
    return Norms

####################################################

def GetNorm(image_name): 
    '''
    Input: image file name
    Output: Normalisation method
    '''
    n = image_name

    Norm = n.split("_")[2]
    Norm = Norm.replace(".nii", "")
    Norm = Norm.replace("v2", "")
    if Norm == "image":
        Norm = "Raw"

    return Norm

####################################################

def GetRegion(mask_name):
    '''
    Input: Mask name
    Output: Mask region
    '''
    n = mask_name

    if "pros" in n:
        Region = "Prostate"
    elif "glute" in n: 
        Region = "Glute"
    elif "psoas" in n:
        Region = "Psoas"
    else:
        Region = "-"
    
    return Region

####################################################

def FixPatID(patID, treatment_group):
    '''
    '''
    if "new" in treatment_group:
        newID = str(patID)
    else:
        if len(str(patID)) == 3:
            newID = "0000" + str(patID)
        elif len(str(patID)) == 4:
            newID = "000" + str(patID)
        else:
            newID = str(patID)

    return newID 

####################################################

def FixDate(date):
    '''
    '''
    date_string = str(date)
    if len(date_string) != 8:
        date_string = date_string[:-2]
    date = datetime.strptime(date_string, "%Y%m%d").date()

    return date
####################################################

def GetNiftiPaths(patient_path, treatment):
    """
    """
    mask_path = os.path.join(patient_path, "Masks\\")

    if treatment == "20fractions":
        mask_labels = ["_shrunk_pros.nii", "_glute2.nii", "_psoas.nii"] # set glute2 for 20fractions
    else:
        mask_labels = ["_shrunk_pros.nii", "_glute.nii", "_psoas.nii"]

    image_roots = ["RawImages\\", "HM-TP\\", "HM-FS\\", "HM-FSTP\\","Norm-Pros\\", "Norm-Glute\\", "Norm-Psoas\\", "Med-Pros\\", "Med-Glute\\", "Med-Psoas\\"]
    #image_roots = ["BaseImages\\", "HM-TP\\","Norm-Psoas\\", "Med-Psoas\\"]

    image_labels = ["Raw", "HM-TP", "HM-FS",  "HM-FSTP", "Norm-Pros","Norm-Glute", "Norm-Psoas", "Med-Pros", "Med-Glute", "Med-Psoas"]
    #image_labels = ["Raw", "HM-TP", "Norm-Psoas", "Med-Psoas"]
    
    image_paths = []
    
    for b in image_roots:
        image_paths.append(os.path.join(patient_path, b))
    
    return mask_path, mask_labels, image_paths, image_labels

####################################################

def GetImageFile(image_path, patient, scan, image_label):
    """
    """
    label = image_label
    #if image_label.__contains__("Raw"):
    #    image_label == "image"
    #if label.__contains__("Norm"):# or label.__contains__("Med"):
    #    label = label + "_v2"
    
    
    file_name = patient + "_" + scan + "_" + label + ".nii"
    file_path = os.path.join(image_path, file_name)

    return file_path, file_name

####################################################