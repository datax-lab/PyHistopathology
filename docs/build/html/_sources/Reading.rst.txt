.. PyHistopathology documentation master file, created by
   sphinx-quickstart on Sun Feb  9 08:14:53 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Denoising
=========

Use WSI_Scanning.readWSI() to read Whole-Slide Images

Usage
=====
readWSI(WSI_path, magnification_level, annotation_file, annonated_level)

Arguments
=========

WSI_path
--------

Path or location of WSI.

magnification_level
-------------------

Level of zoom, for example 40x, 20x, 10x, or 5x. Default magnification level is “20x”.
- Note: if magnification 40x for max zoom level of 20x image an error will be raised.

annotation_file
---------------

Default annotation = None. If annotation are available in a xml file, set annotation_file to be the xml file path.

annonated_level
---------------

If annotation is given then set annotated_level equal to the z-axis of the annotations. Default annotatedlevel is 0.

Return Type
===========
Numpy array of WSI Image (After denoising) with dtype int32

Example
=======
::

    from WSI_Preprocessing.Preprocessing import WSI_Scanning 
    import cv2 
    img,slide_dim = WSI_Scanning.readWSI("example.svs") 
    cv2.imwrite("example.png",img)

