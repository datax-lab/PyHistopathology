from src.Patch import Extraction_slides_with_annotations,Extraction_slides_without_annotations
# from Utilities import inputfolder
import os
import sys, getopt



def DataX_WSI_Patch_extraction(inputsvs, outputfolder, Patch_extraction_creatia = 'random', patch_size=(256, 256), num_of_patches=2000,inputxml = None):
    if inputxml != None:
        Extraction_slides_with_annotations(inputxml, inputsvs, outputfolder, Patch_extraction_creatia, patch_size, num_of_patches)
    else:
        Extraction_slides_without_annotations(inputsvs, outputfolder, Patch_extraction_creatia, patch_size,num_of_patches)
    return
def DataX_WSI_Patch_extraction_folder(inputfolder, outputfolder, Patch_extraction_creatia = 'random', patch_size=(256, 256), num_of_patches=2000,inputxml = None):
    
    files = os.listdir(inputfolder)
   
    for file in files:
        if (os.path.exists("%s/%s" % (outputfolder,file))):
            outputfoldername = "%s/%s" % (outputfolder,file)
        else:
            os.mkdir("%s/%s" % (outputfolder,file))
            outputfoldername = "%s/%s" % (outputfolder,file)

        inputsvs = "%s/%s"%(inputfolder,file)
        
        DataX_WSI_Patch_extraction(inputsvs, outputfoldername, Patch_extraction_creatia="random", patch_size=(256, 256), num_of_patches=2000)
        
    return
def main_patch_extraction(inputsvs, outputfolder, inputfolder, Patch_extraction_creatia = 'random',  patch_size=(256, 256), num_of_patches=2000,inputxml = None):
#     print(inputfolder)
    if inputfolder != None:
        
        DataX_WSI_Patch_extraction_folder(inputfolder, outputfolder, Patch_extraction_creatia = 'random', patch_size=(256, 256), num_of_patches=2000,inputxml = None)
    else:
        
        DataX_WSI_Patch_extraction(inputsvs, outputfolder, Patch_extraction_creatia = 'random', patch_size=(256, 256), num_of_patches=2000,inputxml = None)
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
        opts,args = getopt.getopt(argv,"h:f:i:o:c:s:n:x:")
#         print(opts,args)
        
        if len(opts) == 0:
            
            print('test.py -f <inputfolder> or -i <inputfile>, -o <outputfolder>, -c <Cretria(random or all patches)>, -s <(patchsize)>, -n <num of patches>, -x <inputxml>')
            sys.exit()
                
                
        
#         print(opts)
        for opt, arg in opts:

            if opt == '-h':
                print ('test.py -f <inputfolder> or -i <inputfile>, -o <outputfolder>, -c <Cretria(random or all patches)>, -s <(patchsize)>, -n <num of patches>, -x <inputxml> ')
#                 sys.exit()
            elif opt == "-f":
                inputfolder = arg
               

            elif opt == "-i":
                inputfolder = None
                inputsvs = arg
                
            elif opt == "-o":
                
                outputfolder = arg
            elif opt == "-c":
                Patch_extraction_creatia =  arg
            elif opt == "-s":
                patch_size = arg
            elif opt == "-n":
                num_of_patches = arg
            elif opt == "-x":
                inputxml = arg
#         print(arg)
        main_patch_extraction(inputsvs, outputfolder,inputfolder, Patch_extraction_creatia, patch_size, num_of_patches,inputxml)

    except getopt.GetoptError:
        
        sys.exit()
        
                
                
                
            




            

if __name__ == "__main__":
    main(sys.argv[1:])
#     print("yes")
#     DataX_WSI_Patch_extraction('/home/sharedstorage/TCGA_PT/coadread/TCGA-CM-6163-01A-01-TS1.41695082-c639-4313-8770-bb1c13647bd2.svs', "Temp_stains", Patch_extraction_creatia = None,patch_size=(256, 256))

