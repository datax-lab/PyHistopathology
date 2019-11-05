import numpy as np


from WSI_Scanning import reading_WSI,reading_WSI_with_annotations
from Annotation_parsing import extracting_roi_annotations
from Utilities import stainremover_small_patch_remover,stainremover_small_patch_remover1


def localization_with_roi(inputxml, inputsvs):
    slide_dimensions, slide_img = reading_WSI(inputsvs)
    new_cordinate_list  = extracting_roi_annotations(inputxml,slide_dimensions)

    new_image = reading_WSI_with_annotations(slide_img, new_cordinate_list)
    # print(new_image.shape)
    return new_image

def localization_with_out_roi(inputsvs):

    slide_dimensions, slide_img = reading_WSI(inputsvs)
    slide1 = np.asarray(slide_img, dtype="int32")
    patch_x = 20
#     print(slide1.shape)
    for i in range(int((len(slide1[0]))/patch_x)+1):
        for j in range(int((len(slide1))/patch_x)+1):
            sample_img = slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x]
            sample_img_new = stainremover_small_patch_remover(sample_img,(patch_x,patch_x))
            # print(sample_img_new)
            if sample_img_new is None:
                slide1[j * patch_x:j * patch_x + patch_x, i * patch_x:i * patch_x+ patch_x]  = np.zeros_like(sample_img)
                
            else:
                slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x] = sample_img
        
                
    slide1 = np.where(slide1 != [0, 0, 0], slide1, [255, 255, 255])
    return slide1

