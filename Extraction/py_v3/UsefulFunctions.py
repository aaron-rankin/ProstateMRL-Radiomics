from asyncio.windows_events import NULL
from cmath import nan
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
import statsmodels.tsa.stattools as sts

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

def SABRPats():
    '''
    Returns array of patIDs for SABR 
    '''
    array = ['653', '713', '752', '826', '1088', '1089', '1118', '1303', '1307', '1464', '1029',
 '1302', '1431', '1481', '1540', '1553', '1601', '1642', '829', '955']

    return array

#####################################################

def NormArray():
    """
    Returns array of normalisation factors
    """
    Norms = ["Raw", "HM-FS", "HM-TP", "HM-FSTP", "Med-Pros", "Med-Glute", "Med-Psoas"]
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

def GetNiftiPathsProsSens(patient_path, treatment):
    """
    """
    mask_path = os.path.join(patient_path, "Masks\\")

    masks = os.listdir(mask_path)
    mask_labels = []
    for x in masks:
        if "shrunk_pros" in x[:-7]:
            mask_labels.append(x)

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

def ClusterFtSelection(Cluster_ft_df):
    '''
    Input - df filtered for norm, patient, cluster
    Output - performs cross-correlation within clustered fts and returns ft most strongly correlated with the rest, if more than 2 fts present
    '''
    fts = Cluster_ft_df.FeatureName.unique()
    num_fts = len(fts)
   
    if num_fts > 2:
        vals = {} # stores fts and values
        ccfs = {} # stores cc values for each feature
        mean_ccfs = {} # stores the mean cc value for every feature

        for f in fts:
            ft_df = Cluster_ft_df[Cluster_ft_df["FeatureName"] == f]
            ft_vals = ft_df.FeatureChange.values
            vals[f] = ft_vals
        
        for v in vals:
            ft_1 = vals[v]
            ccfs[v] = v
            ccfs_vals = []

            for u in vals:
                ft_2 = vals[u]
                corr = sts.ccf(ft_1, ft_2)[0] # cross correlation value, index [0] for for 0 lag in csc function
                ccfs_vals.append(corr)
            
            mean_ccfs[v] = np.array(ccfs_vals).mean() # get mean across all cc values for each ft

        ft_selected = max(mean_ccfs, key=mean_ccfs.get) # get max mean cc value and return the feature

    else: 
        ft_selected = NULL

    return ft_selected

####################################################

def ClusterFtSelection2(Cluster_ft_df):
    '''
    Input - df filtered for norm, patient, cluster
    Output - performs cross-correlation within clustered fts and returns ft most strongly correlated with the rest, if more than 2 fts present
    '''
    fts = Cluster_ft_df.FeatureName.unique()
    num_fts = len(fts)
   
    if num_fts > 2:
        vals = {} # stores fts and values
        ccfs = {} # stores cc values for each feature
        mean_ccfs = {} # stores the mean cc value for every feature
        num_sel = np.rint(len(fts) * 0.2)
        
        for f in fts:
            ft_df = Cluster_ft_df[Cluster_ft_df["FeatureName"] == f]
            ft_vals = ft_df.FeatureChange.values
            vals[f] = ft_vals
        
        for v in vals:
            ft_1 = vals[v]
            ccfs[v] = v
            ccfs_vals = []

            for u in vals:
                ft_2 = vals[u]
                corr = sts.ccf(ft_1, ft_2)[0] # cross correlation value, index [0] for for 0 lag in csc function
                ccfs_vals.append(corr)
            
            mean_ccfs[v] = np.array(ccfs_vals).mean() # get mean across all cc values for each ft

        s_mean_ccfs = sorted(mean_ccfs.items(), key=lambda x:x[1], reverse=True)
        sorted_temp = s_mean_ccfs[0:int(num_sel)]
        ft_selected = [seq[0] for seq in sorted_temp]

    else: 
        ft_selected = NULL

    return ft_selected

####################################################
def ClusterLinkedFts(ft, df):
    c = df[df["FeatureName"] == ft]["Cluster"].values[0]

    linked_fts = df[df["Cluster"] == c]["FeatureName"].values
    linked_fts = np.delete(linked_fts, np.where(linked_fts == ft))

    return linked_fts

####################################################
def ClusterSimilarity(fts_1, fts_2):
    '''
    
    '''
    fts_1, fts_2 = list(fts_1), list(fts_2)
    sim_fts = set(fts_1) & set(fts_2)
    num_sim_fts = len(sim_fts)
    
    if len(fts_1) != 0 and len(fts_2) != 0:
        
        ratio_a  = len(sim_fts) / len(fts_1)
        ratio_b = len(sim_fts) / len(fts_2)

        ratio = (ratio_a - ratio_b) 
    else: 
        ratio, ratio_a, ratio_b = 1,1,1
    
    return(num_sim_fts, ratio_a, ratio_b, ratio)

####################################################
