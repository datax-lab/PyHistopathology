import cv2
import math
import numpy as np
import os
from WSI_Preprocessing.Preprocessing.WSI_Scanning import readWSI
import gc
import pprint



def inputfolder(inputfolder):
    files = os.listdir(inputfolder)
    files_list = []
    for i in range(len(files)):
        files_list.append(files[i][:-4])
    return list(set(files_list))



    
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
            cv2.imwrite("/home/skosaraju/CATNet2/temp1.png", img)
            img_bg = cv2.imread("/home/skosaraju/CATNet2/temp1.png", 0)
            if (img_bg.mean() < 245) and (img_bg.mean() > 30):
                return img
            else:
                return None

def stainremover_small_patch_remover1(img,patch_size):
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
            cv2.imwrite("tempN1.png", img)
            img_bg = cv2.imread("tempN1.png", 0)
            if ((img_bg.mean() < 230) and (img_bg.mean() > 20)):
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
        if len(slide_dimensions) == 4:
            print("Highest magnification level is 40x")
            dictx = {"40x":0,"20x":1,"10x":2,"5x":3}
        else:
            if len(slide_dimensions) == 2:
                print("Highest magnification level is 10x")
                dictx = {"10x":0,"5x":1}
            else:
                print("Highest magnification level is 10x")
                dictx = {"5x":0}
                
    return dictx




def black_to_white(img):
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (img[i][j][0] == 0) and (img[i][j][1] == 0) and (img[i][j][2] == 0) :
                img[i][j] = [255,255,255]
    return img



def denoising_using_GaussianBlur(inputsvs,magnification,dictx,patch_size ,upperlimit, lowerlimit,Annotation , Annotatedlevel , Requiredlevel):
    mask = denoising_lowermiginification_guassianblur(inputsvs,magnification,dictx,patch_size ,upperlimit, lowerlimit,Annotation , Annotatedlevel , Requiredlevel)
#     mask = cv2.bitwise_not(mask)
    print("cleanedimage at low maginfication done")
    img,slide_dimensions= readWSI(inputsvs,magnification ,Annotation , Annotatedlevel , Requiredlevel)
    img = mask*img
    img[np.where((img == [0,0,0]).all(axis = 2))] = [255,255,255]
#     print("loading high magnification image")
#     out = np.zeros_like(img)
#     img = np.asarray(img, dtype="int32")
#     cv2.imwrite("check2.png",img)
#     print("cleaning image at high mignification")
#     mask = mask.astype(np.bool)
#     out[mask] = img[mask]
#     cv2.imwrite("check3.png",out)
#     out[np.where((out == [0,0,0]).all(axis = 2))] = [255,255,255]
# #     out = black_to_white(out)
#     print("cleaning WSI done")
#     cv2.imwrite("check4.png",out)
    garbage_collector()
    print("exisiting cleaning")
    return img
        

def denoising_lowermiginification_guassianblur(inputsvs,magnification,dictx,patch_size ,upperlimit, lowerlimit, Annotation , Annotatedlevel , Requiredlevel):
    
    non_black_img,slide_dimen = readWSI(inputsvs,"5x",Annotation , Annotatedlevel , Requiredlevel = Requiredlevel+2)
    #sliden = np.asarray(non_black_img, dtype="int32")
#     magnification = "5x"
    sliden1 = localization_with_GaussianBlur(non_black_img,slide_dimen,patch_size ,upperlimit, lowerlimit,Annotation , Annotatedlevel , Requiredlevel)
#     print("Slide demensions",slide_dimen)
    magnification = magnification
    print(magnification)
    try:
#     cv2.imwrite("check1.png",sliden1)
        sliden2 = mask_generation(sliden1,slide_dimen[dictx[magnification]],mask_generation_c = "G")
    except:
        print("this image has lower magnification then the given magnification, cleaning the image at highest magnification possible")
        sliden2 = mask_generation(sliden1,slide_dimen[0],mask_generation_c = "G")
    
    garbage_collector()
    del(sliden1,non_black_img,slide_dimen)
    return sliden2

def localization_with_GaussianBlur(non_black_img,slide_dimen,patch_size ,upperlimit, lowerlimit,Annotation , Annotatedlevel,Requiredlevel):
#     slide1 = inputsvs
    slide1 =  non_black_img
    slide_dims = slide_dimen 
    patch_x = 20
    for i in range(int((len(slide1[0]))/patch_x)+1):
        for j in range(int((len(slide1))/patch_x)+1):
            sample_img = slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x]
            sample_img_new = GaussianBlur(sample_img,(patch_x,patch_x),upperlimit, lowerlimit,std = 0)
            if sample_img_new is None:
                slide1[j * patch_x:j * patch_x + patch_x, i * patch_x:i * patch_x+ patch_x]  = np.zeros_like(sample_img)     
            else:
                slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x] = sample_img       
    slide1[np.where((slide1 == [0,0,0]).all(axis = 2))] = [255,255,255]
#     slide1 = np.where(slide1 != [0, 0, 0], slide1, [255, 255, 255])
    garbage_collector()
    return slide1

def mask_generation(img,slide_dimen,mask_generation_c = 'G'):
    cv2.imwrite("tempR.png",img)
    img_gray = cv2.imread("tempR.png",0)
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
#     erosionnf = cv2.merge((erosionnf,erosionnf,erosionnf))
#     cv2.imwrite("temp1.png",erosionnf)
#     erosionnf = cv2.imread("temp1.png")
#     os.remove("tempR.png")
#     os.remove("temp1.png")
    erosionnf =  np.asarray(erosionnf, dtype="int32")
#     kernalnew = np.ones((3, 3), np.uint8)
#     kernalnew1 = np.ones((1, 1), np.uint8)
#     img_d = cv2.erode(img_n, kernalnew, iterations=10)
#     img_d = cv2.dilate(img_d, kernalnew1, iterations=5)
    cv2.imwrite("examplee.png",erosionnf)
    binary_map1 = (erosionnf > 200).astype(np.uint8)
    cv2.imwrite("examplee1.png",binary_map1)
    X = cv2.connectedComponentsWithStats(binary_map1, 8)[2][1:]
    output = cv2.connectedComponentsWithStats(binary_map1, 8)[1]
    img2 = np.zeros((output.shape))
    if cv2.connectedComponentsWithStats(binary_map1, 8)[0] > 10:
        print("1,%s"%cv2.connectedComponentsWithStats(binary_map1, 8)[0])
        for i in range(len(X)):
            if X[i,4]>X[:,4].mean():
                img2[output == i + 1] = 255
                cv2.imwrite("exampleee2.png", img2*255)

        #         img_d1 = img[X[i,1] : X[i,1]+X[i,3],X[i,0] : X[i,0]+X[i,2]]
        #         img_d1 = cv2.cvtColor(img_d1, cv2.COLOR_RGB2BGR)

        #         cv2.imwrite("/home/skosaraju/TCGALUAD/nweslides/TCGA-55-A48Z-01Z-00-DX1/%s.png"%i, cv2.cvtColor(np.array(img_d1, dtype = "uint8"), cv2.COLOR_RGB2BGR))
    else:
        print("0,%s"%cv2.connectedComponentsWithStats(binary_map1, 8)[0])
        for i in range(len(X)):
            if X[i,4]>X[:,4].mean():
                img2[output == i + 1] = 255
                cv2.imwrite("exampleee2.png", img2*255)
    img3 = cv2.imread("exampleee2.png")
    img3 = img3/255
    return img3


def GaussianBlur(img,patch_size ,upperlimit, lowerlimit,std):
    cleaned_Images = []
    try:  
        if len(img) < patch_size[1] or len(img[0]) < patch_size[0]:
            return None     
        else:
            cv2.imwrite("temp%s.png"%std, img)
            img_bg = cv2.imread("temp%s.png"%std, 0)
            non = img_bg
            blur_non = cv2.GaussianBlur(non, (11, 11), 2)
            for i in range(20):
                blur_non = cv2.GaussianBlur(blur_non, (11,11), 2)
                last_blur_non = cv2.GaussianBlur(blur_non, (11, 11), 2)
            ssd_blur_non = np.sum((last_blur_non - blur_non)**2)
#             print(ssd_blur_non)
            if ssd_blur_non < upperlimit and ssd_blur_non > lowerlimit - 1:
                return img
            else:
                return None
    except:
        return None
    
def GaussianBlurjpeg(img,patch_size ,upperlimit, lowerlimit,std):
    cleaned_Images = []
    try:  
        if len(img) < patch_size[1] or len(img[0]) < patch_size[0]:
            return None     
        else:
#             print("here")
            cv2.imwrite("temp%s.png"%std, img)
            img_bg = cv2.imread("temp%s.png"%std, 0)
            non = img_bg
            
            blur_non = cv2.GaussianBlur(non, (63, 63), 2)
#             print(b)
            for i in range(20):
                blur_non = cv2.GaussianBlur(blur_non, (63,63), 2)
                last_blur_non = cv2.GaussianBlur(blur_non, (63, 63), 2)
                
            ssd_blur_non = np.sum((last_blur_non - blur_non)**2)
#             print(ssd_blur_non)
            if ssd_blur_non < upperlimit and ssd_blur_non > lowerlimit - 1:
                return img
            else:
                return None
    except:
#         print(a)
        return None

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
        slide1[np.where((slide1 == [0,0,0]).all(axis = 2))] = [255,255,255]
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
#     del(non_black_img,slide_dimen)
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

def denoising_jpeg(img,std = 0,upperlimit =290000, lowerlimit = 1500):
    slide1 = cv2.imread(img)
    patch_x = 256
    for i in range(int((len(slide1[0]))/patch_x)+1):
        for j in range(int((len(slide1))/patch_x)+1):
            sample_img = slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x]
            sample_img_new = GaussianBlurjpeg(sample_img,(patch_x,patch_x),upperlimit, lowerlimit,std)
            if sample_img_new is None:
                slide1[j * patch_x:j * patch_x + patch_x, i * patch_x:i * patch_x+ patch_x]  = np.zeros_like(sample_img)     
            else:
                slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x] = sample_img       
    slide1[np.where((slide1 == [0,0,0]).all(axis = 2))] = [255,255,255]
    garbage_collector()
    cv2.imwrite("temp%sR.png"%std,slide1)
    img_gray = cv2.imread("temp%sR.png"%std,0)
    ret, bw_img = cv2.threshold(img_gray,160,255,cv2. THRESH_BINARY)
    kernel = np.ones((4,4),np.uint8)
    erosion = cv2.erode(bw_img,kernel,iterations = 10)
    erosionnf = cv2.bitwise_not(erosion)
    del (erosion,kernel,ret,img_gray,img)
#     erosionnf = cv2.merge((erosionnf,erosionnf,erosionnf))
#     cv2.imwrite("temp1.png",erosionnf)
#     erosionnf = cv2.imread("temp1.png")
#     os.remove("tempR.png")
#     os.remove("temp1.png")
    erosionnf =  np.asarray(erosionnf, dtype="int32")
#     kernalnew = np.ones((3, 3), np.uint8)
#     kernalnew1 = np.ones((1, 1), np.uint8)
#     img_d = cv2.erode(img_n, kernalnew, iterations=10)
#     img_d = cv2.dilate(img_d, kernalnew1, iterations=5)
#     cv2.imwrite("examplee.png",erosionnf)
    binary_map1 = (erosionnf > 200).astype(np.uint8)
#     cv2.imwrite("examplee1.png",binary_map1)
    X = cv2.connectedComponentsWithStats(binary_map1, 8)[2][1:]
    output = cv2.connectedComponentsWithStats(binary_map1, 8)[1]
    img2 = np.zeros((output.shape))
    if cv2.connectedComponentsWithStats(binary_map1, 8)[0] > 30:
        print("1,%s"%cv2.connectedComponentsWithStats(binary_map1, 8)[0])
        for i in range(len(X)):
            if X[i,4]>X[:,4].mean()*8:
                img2[output == i + 1] = 255
                cv2.imwrite("exampleee%s2.png"%std, img2*255)

        #         img_d1 = img[X[i,1] : X[i,1]+X[i,3],X[i,0] : X[i,0]+X[i,2]]
        #         img_d1 = cv2.cvtColor(img_d1, cv2.COLOR_RGB2BGR)

        #         cv2.imwrite("/home/skosaraju/TCGALUAD/nweslides/TCGA-55-A48Z-01Z-00-DX1/%s.png"%i, cv2.cvtColor(np.array(img_d1, dtype = "uint8"), cv2.COLOR_RGB2BGR))
    else:
        print("0,%s"%cv2.connectedComponentsWithStats(binary_map1, 8)[0])
        for i in range(len(X)):
            if X[i,4]>X[:,4].mean():
                img2[output == i + 1] = 255
                cv2.imwrite("exampleee%s2.png"%std, img2*255)
    img3 = cv2.imread("exampleee%s2.png"%std)
    img3 = img3/255
    img4 = slide1*img3
    img4[np.where((img4 == [0,0,0]).all(axis = 2))] = [255,255,255]
    
#     patch_x = 20
#     for i in range(int((len(slide1[0]))/patch_x)+1):
#         for j in range(int((len(slide1))/patch_x)+1):
#             sample_img = slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x]
#             sample_img_new = GaussianBlur(sample_img,(patch_x,patch_x),upperlimit, lowerlimit)
#             if sample_img_new is None:
#                 slide1[j * patch_x:j * patch_x + patch_x, i * patch_x:i * patch_x+ patch_x]  = np.zeros_like(sample_img)     
#             else:
#                 slide1[j*patch_x:j*patch_x+patch_x,i*patch_x:i*patch_x+patch_x] = sample_img       
#     slide1[np.where((slide1 == [0,0,0]).all(axis = 2))] = [255,255,255]
#     garbage_collector()

    return img4
    