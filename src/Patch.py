import numpy as np
from Localization import localization_with_roi,localization_with_out_roi
from Patch_extraction_creteria import patch_extraction_random,all_patches_extarction
import cv2

def Extraction_slides_with_annotations(inputxml,inputsvs,outpath,Patch_extraction_creatia,patch_size,num_of_patches):
    # inputxml = '%s/%s/%s/%s/%s.xml' % (datapath, project, type, stain, file)
    correctedslide = localization_with_roi(inputxml, inputsvs)
    # correctedslide = cropping_white(correctedslide)
    # print(correctedslide.shape)

    # cv2.imwrite("cropped_slides/%s.png" % file, correctedslide)
    # out_put_path = "/home/skosaraju/%s/%s/%s/%s" % (project, stain,type,  file)
    if Patch_extraction_creatia == 'random':
        patch_extraction_random(correctedslide, outpath,patch_size, num_of_patches)
    else:
        all_patches_extarction(correctedslide, outpath, patch_size)
    # patch_extraction(correctedslide, out_put_path)
    return
def Extraction_slides_without_annotations(inputsvs,outpath,Patch_extraction_creatia,patch_size,num_of_patches):
    slide1 = localization_with_out_roi(inputsvs)
    # slide1 = np.asarray(slide1, dtype="int32")
    cv2.imwrite("localizedslides/example.png",slide1)
    # outpath = "/home/skosaraju/%s/%s/%s/%s" % (project, stain,type,  file)
    if Patch_extraction_creatia == 'random':
        patch_extraction_random(slide1, outpath,patch_size, num_of_patches)
    else:
        all_patches_extarction(slide1, outpath, patch_size)
    # patch_extraction(correctedslide, out_put_path)

    return
