import cv2
import random
from Utilities import stainremover_small_patch_remover,stainremover_small_patch_remover1

import numpy as np
def random_patchcs_with_uniform_distrubutions(img, tile_size):
    img_shape = img.shape

    # img = img[3*int(img_shape[1])/4:,3*int(img_shape[0])/4:]

    # tile_size = (256, 256)
    x_point = random.randint(0, img_shape[0])
    y_point = random.randint(0, img_shape[1])
    try:
        # if (cropped_img.mean() > 50) and (cropped_img.mean() < 180) and (len(list(set(cropped_img.flatten()))) > 50):
        cropped_image = img[x_point:x_point + int(tile_size[0]),y_point:y_point + int(tile_size[1])]

        cleaned_image = stainremover_small_patch_remover1(cropped_image,tile_size)

    except:
        # print(a)
        cleaned_image = None
    #     cv2.imwrite('1.png',cleaned_image)
    return cleaned_image
def reconstructionofwholeslide(slide_dimensions):
    out = np.zeros_like(slide1)
    for i in range():
        mask = np.zeros((slide1.shape[0], slide1.shape[1]))
        cv2.fillConvexPoly(mask, np.array(new_cordinate_list[i]), 1)
        mask = mask.astype(np.bool)

        out[mask] = slide1[mask]

        # out[out == [0,0,0]] =  [255,255,255]
        # cv2.imwrite("example.png",np.array(out))
    out = np.where(out != [0, 0, 0], out, [255,255,255])
    # print('yes')
    return np.array(out)
def all_patches_extarction(slide1, outpath,patch_size):
#     print(len(slide1) / patch_size[1])
#     print(len(slide1[0]) / patch_size[0])
    reconstrcutedimage = np.zeros_like(slide1)
    for i in range(int(len(slide1[0]) / patch_size[1])):
        for j in range(int(len(slide1[1]) / patch_size[0])):
            # print(i,j)
            sample_img = slide1[j * patch_size[0]:j * patch_size[0] + patch_size[0],
                         i * patch_size[1]:i * patch_size[1] + patch_size[1]]
            patchs = stainremover_small_patch_remover1(sample_img, patch_size)
            if patchs is None:
#                 print("i,j")
                None
            else:          
            
                cv2.imwrite('%s/%s_%s.png' % (outpath, i,j), patchs)
                outputImage = cv2.copyMakeBorder(
                 patchs, 5, 5, 5, 5, 
                 cv2.BORDER_CONSTANT, 
                 value=(0,0,255)
              )
                reconstrcutedimage[j * patch_size[0]:j * patch_size[0] + patch_size[0]+10,
                         i * patch_size[1]:i * patch_size[1] + patch_size[1]+10] = outputImage
    reconstrcutedimage  = np.where(reconstrcutedimage != [0, 0, 0],reconstrcutedimage , [255,255,255])
    cv2.imwrite("examplereconstruction.png",reconstrcutedimage)
                

            
    return

def patch_extraction_random(img, outpath,patch_size, num_of_patches):
    # print(img.shape)
    # print(img)
    len_list = []

    # if Patch_extarction_criteria == 'rondom_patches':
    i = 0
    while len(len_list) < num_of_patches:
        patchs = random_patchcs_with_uniform_distrubutions(img, patch_size)
        if patchs is None:
            None
        else:
            # print('here')
            # print('%s/%s.jpg' % (outpath, i))
            cv2.imwrite('%s/%s.png' % (outpath, i), patchs)
            # print("this")
            len_list.append(i)
        i = i+1

    return

    # for i in range(100000):
    #     if len(len_list) < 2000:
    #         patchs = random_croping(img, tile_size)
    #         # print(patchs)
    #         if patchs is None:
    #             None
    #         else:
    #             # print(i)
    #             cv2.imwrite('%s/%s.png' % (outpath, i), patchs)
    #             len_list.append(i)
    #     else:
    #         return
    # return
