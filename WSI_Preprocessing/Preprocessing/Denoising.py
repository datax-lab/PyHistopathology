import cv2
import math
import numpy as np
import os
from WSI_Preprocessing.Preprocessing.WSI_Scanning import readWSI
from WSI_Preprocessing.Preprocessing.Utilities import garbage_collector,denoising_lowermiginification_guassianblur,denoising_RGB_Thersholding,denoising_No_filters,dictionary,denoising_using_GaussianBlur
import openslide
from openslide import (OpenSlide, OpenSlideError,OpenSlideUnsupportedFormatError)


def denoising(inputsvs,magnification = "20x",filtering = "GaussianBlur",patch_size = (256,256),upperlimit = 1100, lowerlimit = 300, red_value = (80,220), green_value = (80,200), blue_value = (80, 170), Annotation = None, Annotatedlevel = 0, Requiredlevel = 0):
    slide = OpenSlide(inputsvs)
    slide_dimensions = slide.level_dimensions
#     img,slide_dimensions= readWSI(inputsvs,magnification,Annotation, Annotatedlevel, Requiredlevel)
    dictx = dictionary(slide_dimensions)
    if filtering == "GaussianBlur":
        out = denoising_using_GaussianBlur(inputsvs,magnification,dictx,patch_size ,upperlimit, lowerlimit,Annotation , Annotatedlevel , Requiredlevel)
    elif filtering == "RGB":
        mask = denoising_RGB_Thersholding(img,slide_dimensions, magnification,dictx,patch_size,red_value,green_value,blue_value)
        out = np.zeros_like(img)
        print("cleaning image at high mignification")
        mask = mask.astype(np.bool)
        out[mask] = img[mask]
        out = np.where(out != [0, 0, 0], out, [255,255,255])
        print("cleaning WSI done")
    #     cv2.imwrite("/home/pagenet2/PageNet2/Data Preprocessing Pipeline/WSI_Precessing_test/cleanedimages/%s/cleanedsmallf.png"%(inputsvs.split("/")[-1][:-4]),out)
        garbage_collector()
        print("exisiting cleaning")
        
    else:
        mask = denoising_No_filters(img,slide_dimensions, magnification,dictx)
        out = np.zeros_like(img)
        print("cleaning image at high mignification")
        mask = mask.astype(np.bool)
        out[mask] = img[mask]
        out = np.where(out != [0, 0, 0], out, [255,255,255])
        print("cleaning WSI done")
    #     cv2.imwrite("/home/pagenet2/PageNet2/Data Preprocessing Pipeline/WSI_Precessing_test/cleanedimages/%s/cleanedsmallf.png"%(inputsvs.split("/")[-1][:-4]),out)
        garbage_collector()
        print("exisiting cleaning")
    return out
