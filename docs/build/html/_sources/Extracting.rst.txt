.. PyHistopathology documentation master file, created by
   sphinx-quickstart on Sun Feb  9 08:14:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Extracting
==========

Use Extractingpatches.extractingPatches() to extract patches from Whole-Slide Images

Usage
=====
extractingPatches(inputsvs, outputpath, magnification, patch_extraction_creatia, number_of_patches, filtering, patch_size, upperlimit, lowerlimit, red_value, green_value, blue_value, Annotation, Annotationlevel, Requiredlevel, reconstructionimagepath)

Arguments
=========

inputsvs
--------

Path or location of WSI.

magnification
-------------

Level of zoom, for example 40, 20, 10, or 5. Default magnification level is 20.
- Note: if magnification 40x for max zoom level of 20x image an error will be raised.

filtering
---------

GuassianBlur, RGBThersholding, or None


GuassianBlur: Homogeneity calculations based on image smoothing and Gaussian blur equations. We compute sum of square differences between two consecutive Gaussian blurred images as score for homogeneity.

* Upper limit: Upper threshold of homogeneity score. Default value is 9500 with kernel size of 1111 
* Lower limit: lower threshold of homogeneity score. default value is 1500 with kernel size of 1111 
* Patch size: Not significant parameters for GuassianBlur filtering
  
RGBThersholding: Validated patches based on RGB values of patches 

* red_value: Red threshold
* green-value: Green threshold
* blue_value: Blue Threshold


None: Only removes Background

Note that our default is GuassianBlur technique. GuassianBlur is highly effective and requires more computational power (RAM). RGBThersholding is less effective which needs less computational power

patch_extraction_creatia
------------------------

random, or None. Default is None. For extracting a fixed number of patches for WSI we can use random.

number_of_patches
-----------------
Default number of patches is 2000

outputpath
----------
Folder to store the extracted patches

reconstructionimagepath
-----------------------
If you want to compare the patches with WSI we can mention the reconstructionimagepath. Default is None.
Note: it only works with patch_extraction_creatia = None.



Return Type
===========
None, fills up output path with images directly instead of returning a Numpy array.


