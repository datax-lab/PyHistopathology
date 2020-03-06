import cv2
import math
import numpy as np
import os
from Preprocessing.WSI_Scanning import readWSI
import gc
import pprint

def localization_with_GaussianBlur(inputsvs,img,patch_size ,upperlimit, lowerlimit):
    slide1 = inputsvs
    slide1, slide_dims = readWSI(inputsvs)
    patch_x = 20
    for i in range(int((len(slide1[0]))/patch_x)+1):
        for j in range(int((len(slide1))/patch_x)+1):
            sample_img = slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x]
            sample_img_new = GaussianBlur(sample_img,(patch_x,patch_x),upperlimit, lowerlimit)
            if sample_img_new is None:
                slide1[j * patch_x:j * patch_x + patch_x, i * patch_x:i * patch_x+ patch_x]  = np.zeros_like(sample_img)     
            else:
                slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x] = sample_img       
    slide1 = np.where(slide1 != [0, 0, 0], slide1, [255, 255, 255])
    garbage_collector()
    return slide1

def inputfolder(inputfolder):
    files = os.listdir(inputfolder)
    files_list = []
    for i in range(len(files)):
        files_list.append(files[i][:-4])
    return list(set(files_list))


def GaussianBlur(img,patch_size ,upperlimit, lowerlimit):
    cleaned_Images = []
    try:  
        if len(img) < patch_size[1] or len(img[0]) < patch_size[0]:
            return None     
        else:
            cv2.imwrite("temp0.png", img)
            img_bg = cv2.imread("temp0.png", 0)
            non = img_bg
            blur_non = cv2.GaussianBlur(non, (11, 11), 2)
            for i in range(20):
                blur_non = cv2.GaussianBlur(blur_non, (11,11), 2)
                last_blur_non = cv2.GaussianBlur(blur_non, (11, 11), 2)
            ssd_blur_non = np.sum((last_blur_non - blur_non)**2)
            if ssd_blur_non < upperlimit and ssd_blur_non > lowerlimit:
                return img
            else:
                return None
    except:
        return None
def RGB_Thersholding(img,patch_size,red_value, green_value, blue_value):
    if len(img) < patch_size[1] or len(img[0]) < patch_size[0]:
        return None
    else:
        Xb = []
        Xg = []
        Xr = []
        for i in range(len(img)):
            Xb.append(np.mean(img[i][:, 0]))
            Xg.append(np.mean(img[i][:, 1]))
            Xr.append(np.mean(img[i][:, 2]))
        if np.mean(Xr) < red_value[0] or np.mean(Xr) > red_value[1] :
            return None
        elif np.mean(Xg) < green_value[0] or np.mean(Xg) > green_value[1]:
             return None
        elif np.mean(Xb) < blue_value[0] or np.mean(Xb) > blue_value[1]:
            return None
        else:
            cv2.imwrite("temp0.png", img)
            img_bg = cv2.imread("temp0.png", 0)
            if (img_bg.mean() < 220) and (img_bg.mean() > 50):
                return img
            else:
                return None

def stainremover_small_patch_remover1(img,patch_size = (256,256)):
    if len(img) < patch_size[1] or len(img[0]) < patch_size[0]:
        return None
    else:
        Xb = []
        Xg = []
        Xr = []
        for i in range(len(img)):
            Xb.append(np.mean(img[i][:, 0]))
            Xg.append(np.mean(img[i][:, 1]))
            Xr.append(np.mean(img[i][:, 2]))
        if np.mean(Xr) < 0 or np.mean(Xr) > 255:
            return None
        elif np.mean(Xg) < 0 or np.mean(Xg) > 255:
             return None
        elif np.mean(Xb) < 0 or np.mean(Xb) > 255:
            return None
        else:
            cv2.imwrite("temp0.png", img)
            img_bg = cv2.imread("temp0.png", 0) 
            if (img_bg.mean() < 240) and (img_bg.mean() > 10):
                return img
            else:
                return None

def making_one_image(inputfolder):  
    img1 = cv2.imread("%s/1.png"%(inputfolder))
    img2 = cv2.imread("%s/2.png"%(inputfolder))
    img3 = cv2.imread("%s/3.png"%(inputfolder))
    img4 = cv2.imread("%s/4.png"%(inputfolder))
    img5 = np.concatenate([img1,img2], axis =1)
    img6 = np.concatenate([img3,img4], axis =1 )
    img7 = np.concatenate([img5,img6], axis =0 )
    cv2.imwrite("%s/final.png"%(inputfolder),img7)
    return       
       
def mask_generation(img,slide_dimen,mask_generation_c = 'G'):
    cv2.imwrite("temp.png",img)
    img_gray = cv2.imread("temp.png",0)
    ret, bw_img = cv2.threshold(img_gray,160,255,cv2. THRESH_BINARY)
    kernel = np.ones((2,2),np.uint8)
    erosion = cv2.erode(bw_img,kernel,iterations = 10)
#     print(slide_dimen[0],slide_dimen[1])
#     erosion = np.asarray(erosion,dtype = 'uint8')
    if slide_dimen[0]*slide_dimen[1] > 2**31:
        
        erosionn = split_up_resize(erosion, slide_dimen)
    else:
        erosionn = cv2.resize(erosion, slide_dimen)
    erosionnf = cv2.bitwise_not(erosionn)
    del (erosion,kernel,ret,img_gray,img)
    erosionnf = cv2.merge((erosionnf,erosionnf,erosionnf))
#     cv2.imwrite("temp1.png",erosionnf)
#     erosionnf = cv2.imread("temp1.png")
    os.remove("temp.png")
#     os.remove("temp1.png")
    erosionnf =  np.asarray(erosionnf, dtype="int32")
    return erosionnf

def reading_image_at_low_magnification(inputsvs):
    slide,slide_dimen = reading_WSI(inputsvs,maginification="5x")
    return slide,slide_dimen

def garbage_collector():
    for j in range(2):
        n = gc.collect()
    return

def dictionary(slide_dimensions):
    if len(slide_dimensions) == 3:
        print("Highest magnification level is 20x")
        dictx = {"20x":0,"10x":1,"5x":2}
    else:
        print("Highest magnification level is 40x")
        dictx = {"40x":0,"20x":1,"10x":2,"5x":3}
    return dictx








def denoising_using_GaussianBlur(inputsvs,magnification,img,dictx,patch_size ,upperlimit, lowerlimit):
    mask = denoising_lowermiginification_guassianblur(inputsvs,magnification,dictx,patch_size ,upperlimit, lowerlimit)
#     mask = cv2.bitwise_not(mask)
    print("cleanedimage at low maginfication done")
#     img,slide_dimensions= reading_WSI(inputsvs,maginification="20x")
    print("loading high magnification image")
    out = np.zeros_like(img)
    img = np.asarray(img, dtype="int32")
    cv2.imwrite("/home/pagenet2/PageNet2/Final_Package/orginalimage/%s.png"%(inputsvs.split("/")[-1][:-4]),img)
    print("cleaning image at high mignification")
    mask = mask.astype(np.bool)
    out[mask] = img[mask]
    out = np.where(out != [0, 0, 0], out, [255,255,255])
    print("cleaning WSI done")
    cv2.imwrite("/home/pagenet2/PageNet2/Final_Package/cleanedimages/%s.png"%(inputsvs.split("/")[-1][:-4]),out)
    garbage_collector()
    print("exisiting cleaning")
    return out
        

def denoising_lowermiginification_guassianblur(inputsvs,magnification,dictx,patch_size ,upperlimit, lowerlimit):
    non_black_img,slide_dimen = readWSI(inputsvs,magnification = "5x")
    #sliden = np.asarray(non_black_img, dtype="int32")
    sliden1 = localization_with_GaussianBlur(inputsvs,non_black_img,patch_size ,upperlimit, lowerlimit)
#     print("Slide demensions",slide_dimen)

    sliden2 = mask_generation(sliden1,slide_dimen[dictx[magnification]],mask_generation_c = "G")
    garbage_collector()
    del(sliden1,non_black_img,slide_dimen)
    return sliden2

def localization_RGB_Thersholding(inputsvs,patch_size,magnification,red_value,green_value,blue_value):
        slide1 = inputsvs
        patch_x = patch_size[0]
        for i in range(int((len(slide1[0]))/patch_x)+1):
            for j in range(int((len(slide1))/patch_x)+1):
                sample_img = slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x]
                sample_img_new = RGB_Thersholding(sample_img, patch_size, red_value, green_value, blue_value)
                if sample_img_new is None:
                    slide1[j * patch_x:j * patch_x + patch_x, i * patch_x:i * patch_x+ patch_x]  = np.zeros_like(sample_img)
                else:
                    slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x] = sample_img
        slide1 = np.where(slide1 != [0, 0, 0], slide1, [255, 255, 255])
        garbage_collector()
        return slide1
def denoising_RGB_Thersholding(inputsvs,slide_dimen,magnification,dictx):
    
    #non_black_img,slide_dimen = readWSI(inputsvs,magnification)
    sliden1 = localization_RGB_Thersholding(inputsvs,patch_size,red_value, green_value, blue_value)
    sliden2 = mask_generation(sliden1,slide_dimen[dictx[magnification]],mask_generation_c = "L")
    garbage_collector()
    del(sliden1,non_black_img,slide_dimen)
    return sliden2
def denoising_No_filters(inputsvs,slide_dimen,magnification,dictx):
    #non_black_img,slide_dimen = readWSI(inputsvs,magnification)
    sliden2 = mask_generation(inputsvs, slide_dimen[dictx[magnification]], mask_generation_c = "L")
    del(non_black_img,slide_dimen)
    return sliden2



def split_up_resize(arr, res):
    res_1 = (res[0], math.ceil(res[1]/2))
    res_2 = (res[0], res[1] - math.ceil(res[1]/2))
    arr_1 = arr[0 : math.ceil(len(arr)/2)]
    arr_2 = arr[math.ceil(len(arr)/2) :]

    arr_1 = cv2.resize(arr_1, res_1)
    arr_2 = cv2.resize(arr_2, res_2)

    arr = np.zeros((res[1], res[0]))
    

    arr[0 : math.ceil(len(arr)/2)] = arr_1
    arr[math.ceil(len(arr)/2) :] = arr_2
    del(arr_1,arr_2)
    garbage_collector()
    return arr

