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
def ImageArray(image_url):
    '''
    Gives masked image array
    Input - image path and mask path
    Output - masked image
    '''
    image = sitk.ReadImage(image_url)
    image_array = sitk.GetArrayFromImage(image)

    return image_array
####################################################
def MaskedImage(image_url, mask_url):
    '''
    Gives masked image array
    Input - image path and mask path
    Output - masked image
    '''
    image = sitk.ReadImage(image_url)
    image_array = sitk.GetArrayFromImage(image)
    
    mask = sitk.ReadImage(mask_url)
    mask_array = sitk.GetArrayFromImage(mask) 
    mask_array = mask_array / (np.max(mask_array)) # so masks are 0/1

    masked_image = ma.array(image_array, mask=np.logical_not(mask_array), keep_mask=False, hard_mask=True)

    return masked_image
    
####################################################

def MaskedMeanStd(image_url, mask_url):
    '''
    Returns mean and std of masked image
    Input - image path and mask path
    Output - mean and std (floats)
    '''

    image = sitk.ReadImage(image_url)
    image_array = sitk.GetArrayFromImage(image)
    
    mask = sitk.ReadImage(mask_url)
    mask_array = sitk.GetArrayFromImage(mask) 
    mask_array = mask_array / (np.max(mask_array))
    if image_array.shape != mask_array.shape:
        mean = np.nan
        std = np.nan
    
    else:
        masked_image = ma.array(image_array, mask=np.logical_not(mask_array), keep_mask=False, hard_mask=True)
        mean = ma.mean(masked_image)
        std = ma.std(masked_image)

    return mean, std

####################################################

def DateDifference(date1, date2):
    '''
    Returns difference between two dates from WM (Format Y/M/D) (year incorrect)
    Finds difference and converts to days

    Input - 2 dates (datetiemeobjects)
    Output - Number of days (ints)
    '''
    d1, d2 = date1, date2

    #d1 = datetime.strptime(d1, "%Y-%m-%d")
    #d2 = datetime.strptime(d2, "%Y-%m-%d")

    return abs((d2 - d1).days)

####################################################

def GetNorm(image_name): 
    '''
    Input: image file name
    Output: Normalisation method
    '''
    n = image_name

    if "reg" or "image" in n:
        Norm = "Raw"
    elif "Norm-Pros" in n:
        Norm = "Norm-Pros"
    elif "Norm-Glute" in n:
        Norm = "Norm-Glute"
    elif "Norm-Psoas" in n:
        Norm = "Norm-Psoas"
    elif "HM-TP" in n:
        Norm = "HM-TP"
    elif "HM-FS" in n:
        Norm = "HM-FS"
    else:
        Norm = "-"
    
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

