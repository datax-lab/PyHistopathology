#!/usr/bin/env python
from WSI_Preprocessing.Preprocessing import Extarctingpatches
import os
import sys, getopt



# def DataX_WSI_Patch_extraction(inputsvs, outputfolder, Patch_extraction_creatia = None, patch_size=(256, 256), num_of_patches=2000,inputxml = None):
#     if inputxml != None:
#         Extraction_slides_with_annotations(inputxml, inputsvs, outputfolder, Patch_extraction_creatia, patch_size, num_of_patches)
#     else:
#         Extraction_slides_without_annotations(inputsvs, outputfolder, Patch_extraction_creatia, patch_size,num_of_patches)
#     return

def WSI_Patch_extraction_folder(inputfolder, outputpath,magnification,patch_extraction_creatia = None,num_of_patches = 2000, filtering = "GaussianBlur",patch_size = (256,256),upperlimit = 900, lowerlimit = 300,red_value = (80,220), green_value = (80,200), blue_value = (80, 170),  reconstructedimagepath = None, Annotation = None, Annotatedlevel = 0, Requiredlevel = 0):
    files = os.listdir(inputfolder) 
    for file in files:
        if (os.path.exists("%s/%s" % (outputfolder,file))):
            outputfoldername = "%s/%s" % (outputfolder,file)
        else:
            os.mkdir("%s/%s" % (outputfolder,file))
            outputfoldername = "%s/%s" % (outputfolder,file)
        inputsvs = "%s/%s"%(inputfolder,file)
        Extarctingpatches.extractingPatches(inputsvs,outputpath,magnification,patch_extraction_creatia = None,num_of_patches = 2000, filtering = "GaussianBlur",patch_size = (256,256),upperlimit = 900, lowerlimit = 300,red_value = (80,220), green_value = (80,200), blue_value = (80, 170),  reconstructedimagepath = None, Annotation = None, Annotatedlevel = 0, Requiredlevel = 0)
    return

def main_patch_extraction(inputsvs,outputpath,inputfolder,magnification,patch_extraction_creatia = None,num_of_patches = 2000, filtering = "GaussianBlur",patch_size = (256,256),upperlimit = 900, lowerlimit = 300,red_value = (80,220), green_value = (80,200), blue_value = (80, 170),  reconstructedimagepath = None, Annotation = None, Annotatedlevel = 0, Requiredlevel = 0):
    if inputfolder != None:       
        DataX_WSI_Patch_extraction_folder(inputfolder, outputfolder, Patch_extraction_creatia = None, patch_size=(256, 256), num_of_patches=2000,inputxml = None)
    else:
        Extarctingpatches.extractingPatches(inputsvs,outputpath,magnification,patch_extraction_creatia = None,num_of_patches = 2000, filtering = "GaussianBlur",patch_size = (256,256),upperlimit = 900, lowerlimit = 300,red_value = (80,220), green_value = (80,200), blue_value = (80, 170),  reconstructedimagepath = None, Annotation = None, Annotatedlevel = 0, Requiredlevel = 0)
    return 
      
def main(argv):
    inputfolder = None
    inputsvs = ''
    outputfolder = ''
    Patch_extraction_creatia = None
    patch_size = (256,256)
    num_of_patches =  2000
    inputxml = None
    
    try:
        opts,args = getopt.getopt(argv,"h:f:i:o:c:s:n:a:fi:ul:ll:rv:bv:gv:rpath:al:rl:m")       
        if len(opts) == 0:
            print('WSI_Patch_Extraction.py.py -f <inputfolder> or -i <inputfile>, -o <outputfolder>, -c <Cretria(random or all patches)>, -s <(patchsize)>, -n <num of patches>, -a <inputxml>, -f <filtering technique>, -ul <upperlimit in GB>, -ll <lowerlimit in GB>, -rv <red value in RGB>, -bv <blue value in RGB> , -gv <greenvalue in RGB>, -rpath <reconstruted image path>, -al <annotation level>, -rl <required level>,  -m <magnification>')
            sys.exit()
        for opt, arg in opts:
            if opt == '-h':
                print('WSI_Patch_Extraction.py -f <inputfolder> or -i <inputfile>, -o <outputfolder>, -c <Cretria(random or all patches)>, -s <(patchsize)>, -n <num of patches>, -a <inputxml>, -f <filtering technique>, -ul <upperlimit in GB>, -ll <lowerlimit in GB>, -rv <red value in RGB>, -bv <blue value in RGB> , -gv <greenvalue in RGB>, -rpath <reconstruted image path>, -al <annotation level>, -rl <required level>, -m <magnification>')
                inputfolder = arg              
            elif opt == "-i":
                inputfolder = None
                inputsvs = arg              
            elif opt == "-o":
                outputpath = arg
            elif opt == "-c":
                Patch_extraction_creatia =  arg
            elif opt == "-s":
                patch_size = arg
            elif opt == "-n":
                num_of_patches = arg
            elif opt == "-a":
                Annotation = arg
            elif opt == "-fi":
                filtering = arg
            elif opt == "-ul":
                upperlimit = arg
            elif opt == "-ll":
                lowerlimit = arg
            elif opt == "-rv":
                red_value =  arg
            elif opt == "-bv":
                blue_value =  arg
            elif opt == "-gv":
                green_value =  arg
            elif opt == "-rpath":
                reconstructedimagepath = arg
            elif opt == "-al":
                Annotatedlevel = arg
            elif opt == "-rl":
                Requiredlevel = arg
            elif opt == "-m":
                magnification = arg
                
                
                
            
            
                
                
                
                
                
                
        main_patch_extraction(inputsvs,outputpath,inputfolder,magnification = "20x",patch_extraction_creatia = None,num_of_patches = 2000, filtering = "GaussianBlur",patch_size = (256,256),upperlimit = 900, lowerlimit = 300,red_value = (80,220), green_value = (80,200), blue_value = (80, 170),  reconstructedimagepath = None, Annotation = None, Annotatedlevel = 0, Requiredlevel = 0)
    except getopt.GetoptError:
        
        sys.exit()


            

if __name__ == "__main__":
    main(sys.argv[1:])

