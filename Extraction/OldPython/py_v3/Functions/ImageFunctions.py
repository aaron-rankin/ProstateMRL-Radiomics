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

def MaskedMeanMed(image_url, mask_url):
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
        med = np.nan
    
    else:
        masked_image = ma.array(image_array, mask=np.logical_not(mask_array), keep_mask=False, hard_mask=True)
        mean = ma.mean(masked_image)
        masked_image = masked_image[~masked_image.mask]
        med = ma.median(masked_image)
        std = ma.std(masked_image)
        #P90 = ma.percentile(masked_image, 90)
       
    #print(mean, med, std)#, P90)
    return mean, med


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
    
    else:
        masked_image = ma.array(image_array, mask=np.logical_not(mask_array), keep_mask=False, hard_mask=True)
        mean = ma.mean(masked_image)
        std = ma.std(masked_image)
        
       
    return mean, std#, perc

####################################################

def RescaleImage(image_path, factor, output_path):
    '''
    Scales image according to a factor for normalisation
    and writes it out
    Input - image, factor, outpath
    Output - writes image
    '''

    image = sitk.ReadImage(image_path)
    image_array = sitk.GetArrayFromImage(image)

    norm_image_array = image_array * factor

    norm_image = sitk.GetImageFromArray(norm_image_array)
    norm_image.SetDirection(image.GetDirection())
    norm_image.SetSpacing(image.GetSpacing())
    norm_image.SetOrigin(image.GetOrigin())

    sitk.WriteImage(norm_image,output_path)

####################################################

def MaskValue(mask_name):
    '''
    Input: Mask name
    Output: Mask value
    '''
    n = mask_name

    if "pros" in n:
        value = int(255)
    elif "glute" or "psoas" in n: 
        value = int(13)
    
    return value

####################################################