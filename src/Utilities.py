import cv2
import math
import numpy as np
import os
def inputfolder(inputfolder):
    files = os.listdir(inputfolder)
    files_list = []
    for i in range(len(files)):
        files_list.append(files[i][:-4])

    return list(set(files_list))


def stainremover_small_patch_remover(img,patch_size = (256,256),upperlimit = 10000, lowerlimit = 700):
    cleaned_Images = []
    # print(img)
    # print((img.mean()))
    # img = cv2.imread(inputimage)
    # img = cv2.imread(inputimage,0)
#     try:
   
    try:
        
        if len(img) < patch_size[1] or len(img[0]) < patch_size[0]:
            return None
            
#         #
        else:
#             print("lessdemsion")
            cv2.imwrite("temp0.png", img)

            img_bg = cv2.imread("temp0.png", 0)
            #     gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
            non = img_bg

#             print(non.shape)
            blur_non = cv2.GaussianBlur(non, (7, 7), 2)
                # blur_uni = cv2.GaussianBlur(uni, (11, 11), 2)

            for i in range(20):
                blur_non = cv2.GaussianBlur(blur_non, (7,7), 2)
                #     blur_uni = cv2.GaussianBlur(blur_uni, (11, 11), 2)

                last_blur_non = cv2.GaussianBlur(blur_non, (7, 7), 2)
                # last_blur_uni = cv2.GaussianBlur(blur_uni, (11, 11), 2)

            ssd_blur_non = np.sum((last_blur_non - blur_non)**2)
            # ssd_blur_uni = np.sum((last_blur_uni - blur_uni)**2)
#             print(ssd_blur_non)
            if ssd_blur_non < upperlimit and ssd_blur_non > lowerlimit:
                return img
            else:
                return None


    except:
        return None
def stainremover_small_patch_remover1(img,patch_size = (256,256)):
#     print('SSD Non-uniform: %f' % ssd_blur_non)
#     # print('SSD Uniform:     %f' % ssd_blur_uni
    
    if len(img) < patch_size[1] or len(img[0]) < patch_size[0]:
        #         print("lessdemsion")
        return None
        # print(inputimage)
        # os.remove(inputimage)
    else:
        # print('here')
        Xb = []
        Xg = []
        Xr = []
        for i in range(len(img)):
            Xb.append(np.mean(img[i][:, 0]))
            Xg.append(np.mean(img[i][:, 1]))
            Xr.append(np.mean(img[i][:, 2]))
        #     print(inputimage)
        # print(np.mean(Xr),np.mean(Xg),np.mean(Xb))

        if np.mean(Xr) < 0 or np.mean(Xr) > 255:
            # print(np.mean(Xr))
            # print("red")
            #             print(inputimage.split('/')[-1])
            return None
            # print(inputimage)
            # os.remove(inputimage)

        elif np.mean(Xg) < 0 or np.mean(Xg) > 255:
            # print("green")
            return None
            # print(inputimage)
            # os.remove(inputimage)

        elif np.mean(Xb) < 0 or np.mean(Xb) > 255:
            # print("blue")
            return None
        else:
            cv2.imwrite("temp0.png", img)

            img_bg = cv2.imread("temp0.png", 0)
            # print('here')

      
            # img_bg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if (img_bg.mean() < 220) and (img_bg.mean() > 50):

                return img

            else:


#                 print("Blackandwhite")
                return None





