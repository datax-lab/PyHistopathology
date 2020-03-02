# Python Package: PyHistopathology

Read our documentation at https://pyhistopathology.readthedocs.io/en/latest/

## Command line tool:
python3 WSI_PATCH_Extraction.py -args
Mandatory args 
- -i: input svs file path
- -o: output folder path
- -f: input folder for path
    - Note: you should use either -i or -f, cannot use both.
Additional args
- -c: criteria
    - criteria: Random or None, Default is None
- -s: patch size
    - Size of the patch to extract, default is (256,256)
- -n: number of patches
    - Only should be given for -c Random. Default value is 2000.
- -a: input xml
    - if annotations are provided annotations file path should be given. Otherwise don't use this arg.
    
# Package Usage:
## Reading WSI
**Description**
- use WSI_Scanning.readWSI() to read an WSI Image
- Input: WSI path or directory
- Output: functioning numpy array of WSI Image with dtype int32
 **Function**
- readWSI(WSI_path, magnification_level, annotation_file, annonated_level)
     Arguments
    
     - WSI_path: Directory of WSI
-    - magnification_level: level of zoom, example (40x,20x,10x,5x). Default magnification is **“20x”** 
             - Note if magnification 40x for max zoom level of 20x image an error will be raised.
     - annotation_file: Default annotation = None. if annotation are available in xml formats. use annotation = inputxml file path.
     - annonated_level= if annotation is not giving no need to consider this variable. if annotation is given then mention z-axis of annotations. Default annotatedlevel =0
     ```
        ###Reading image example
        from WSI_Preprocessing.Preprocessing import WSI_Scanning 
        import cv2 
        img,slide_dim = WSI_Scanning.readWSI("example.svs") 
        cv2.imwrite("example.png",img)
     ```
        
![](https://paper-attachments.dropbox.com/s_FDB48527FA5ECB7BD9C0FF3FE49E25C14783C24594EC3FBA01AC4BD504920652_1574801775409_example.PNG)

         
     
## Denoising WSI

Description

use Denoising.denoising() to remove stains, folds and other background noise in WSI
-  input: WSI Path or directory 
- Output: functioning numpy array of WSI Image (After denoising) with dtype int32.

Function

denoising(inputsvs, magnification, filtering, patch_size, upperlimit, lowerlimit, red_value, green_value, blue_value)
 Arguments
 - inputsvs: path or location of WSI.
 - magnification: level of zoom, example (40x,20x,10x,5x). Default magnification is **“20x”** 
   - Note if magnification 40x for max zoom level of 20x image an error will be raised.
 - filtering: GuassianBlur, RGBThersholding, None
   - GuassianBlur: Homogeneity calculations based on image smoothing and Gaussian blur equations. 
          We compute sum of  square differences between two consecutive  Gaussian blurred images as score for homogeneity  
         - Upper limit: upper threshold of homogeneity score. default value is 9500 with kernel size of 11*11
         - lower limit: lower threshold of homogeneity score. default value is 1500 with kernel size of 11*11
         - Patch size: Not significant parameters for GuassianBlur filtering
   - RGBThersholding: 
         Validated patches based on RGB values of patches
         - red_value, green-value, blue_values are threshold for RGB
 -  - None:
          Only removes Background
 - - Note that our default is GuassianBlur technique. GuassianBlur is highly effective and requires more computational power (RAM). RGBThersholding is less effective which needs less computational power 

~~~from WSI_Preprocessing.Preprocessing import Denoising 
import cv2 
# Here mandatory options are example.svs and magniﬁcation 
img = Denoising.denoising("example.svs", "20x" ) 
cv2.imwrite("example.png",img)
~~~
![](https://paper-attachments.dropbox.com/s_FDB48527FA5ECB7BD9C0FF3FE49E25C14783C24594EC3FBA01AC4BD504920652_1575319269525_example2.PNG)

# Extracting Patches

Description

use Extractingpatches.extractingPatches() to extract patches from WSI.
- input: WSI Path or directory 
- output: patches from WSI.

Function:
extractingPatches(inputsvs, outputpath, magnification, patch_extraction_creatia, number_of_patches, filtering, patch_size, upperlimit, lowerlimit, red_value, green_value, blue_value, Annotation, Annotationlevel, Requiredlevel, reconstructionimagepath)

 Arguments
    - inputsvs, magnification, patch_extraction_creatia, filtering, patch_size, upperlimit, lowerlimit, red_value, green_value, blue_value, Annotation, Annotationlevel, Requiredlevel, arguments is same as denosing module.
    - patch_extraction_creatia: random, None
    -      - Default is None.
     For extracting a fixed number of patches for WSI we can use random.
    - Default number of patches is 2000
    - outputpath: folder to store the extracted patches
    - reconstructionimagepath: we you want to compare the patches with WSI we can mention the reconstructionimagepath.
     - Default is None
    - - Note: it only works with patch_extraction_creatia = None.
   - - Note: For WSI number of patches can exceed 20k.
```##patch extarction and reconstruction example
from WSI_Preprocessing.Preprocessing import Extarctingpatches
import cv2 
img = Extarctingpatches.extractingPatches("example.svs","temp" ,"20x" ) 
cv2.imwrite("exampler.png",img)
     # Here mandatory options are example.svs and magnification, and outputpath 
Extractingpatches.extractingPatches(example.svs, outputpath, magnification)
```
![](https://paper-attachments.dropbox.com/s_FDB48527FA5ECB7BD9C0FF3FE49E25C14783C24594EC3FBA01AC4BD504920652_1575341759963_Example+Image.PNG)

    
        
                
    



                
        


