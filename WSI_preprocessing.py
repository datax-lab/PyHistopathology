import openslide
from openslide import (OpenSlide, OpenSlideError,
                       OpenSlideUnsupportedFormatError)
import re
import sys
import PIL
import numpy as np
import os
from PIL import Image, ImageDraw
from openslide.deepzoom import DeepZoomGenerator as dz
import cv2
import math
import pandas as pd


import random
from Annotation_parsing import extracting_cancers_regions_annotations

def reading_WSI(slide_path):
    slide = OpenSlide(slide_path)
    slide_dimensions = slide.level_dimensions
    slide_img = slide.read_region((0, 0), 1, (slide.level_dimensions[1][0], slide.level_dimensions[1][1])).convert(
        'RGB')
    print(slide_dimensions, slide_img)
    return slide_dimensions, slide_img




def cropping_roi(slide_img, new_cordinate_list):
    slide1 = np.asarray(slide_img, dtype="int32")

    out = np.zeros_like(slide1)
    for i in range(len(new_cordinate_list)):
        mask = np.zeros((slide1.shape[0], slide1.shape[1]))
        cv2.fillConvexPoly(mask, np.array(new_cordinate_list[i]), 1)
        mask = mask.astype(np.bool)

        out[mask] = slide1[mask]

        # out[out == [0,0,0]] =  [255,255,255]
        # cv2.imwrite("example.png",np.array(out))
    out = np.where(out != [0, 0, 0], out, [255, 255, 255])
    return np.array(out)





def cropping_main(inputxml, inputsvs):
    slide_dimensions, slide_img = reading_WSI(inputsvs)
    new_cordinate_list  = extracting_cancers_regions_annotations(inputxml,slide_dimensions)

    new_image = cropping_roi(slide_img, new_cordinate_list)
    return new_image


def stainremover_small_patch_remover(img):
    cleaned_Images = []
    # print(img)

    # img = cv2.imread(inputimage)
    # img = cv2.imread(inputimage,0)
    if len(img) < 256 or len(img[0]) < 256:
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

        if np.mean(Xr) < 70 or np.mean(Xr) > 220:
            # print(np.mean(Xr))
            # print("red")
            #             print(inputimage.split('/')[-1])
            return None
            # print(inputimage)
            # os.remove(inputimage)

        elif np.mean(Xg) < 80 or np.mean(Xg) > 200:
            # print("green")
            return None
            # print(inputimage)
            # os.remove(inputimage)

        elif np.mean(Xb) < 100 or np.mean(Xb) > 210:
            # print("blue")
            return None
        else:
            # print('here')

            cv2.imwrite("temp0.png", img)
            img_bg = cv2.imread("temp0.png", 0)
            # img_bg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            if (img_bg.mean() < 215) and (img_bg.mean() > 50):

                return img

            else:
                # print((img_bg.mean()))

                # print("Blackandwhite")
                return None


def random_croping(img, tile_size):
    img_shape = img.shape
    # tile_size = (256, 256)
    x_point = random.randint(0, img_shape[0])
    y_point = random.randint(0, img_shape[1])
    try:
        # if (cropped_img.mean() > 50) and (cropped_img.mean() < 180) and (len(list(set(cropped_img.flatten()))) > 50):
        cropped_image = img[y_point:y_point + 256, x_point:x_point + 256]

        cleaned_image = stainremover_small_patch_remover(cropped_image)

    except:
        # print(a)
        None
    #     cv2.imwrite('1.png',cleaned_image)
    return cleaned_image


def path_extraction(img, path):
    tile_size = (256, 256)
    # print(img)
    len_list = []
    for i in range(100000):

        patchs = random_croping(img, tile_size)

        if len(len_list) < 2000:
            # print(patchs)

            if patchs is None:
                None
            else:
                # print(i)
                cv2.imwrite('%s/%s.png' % (path, i), patchs)
                len_list.append(i)

        else:

            return
    return


def inputfolder(inputfolder):
    files = os.listdir(inputfolder)
    files_list = []
    for i in range(len(files)):
        files_list.append(files[i][:-4])

    return list(set(files_list))


# print(files)
def cancer_region_extraction(inputxml,inputsvs,project,stain,type,file):
    # inputxml = '%s/%s/%s/%s/%s.xml' % (datapath, project, type, stain, file)
    correctedslide = cropping_main(inputxml, inputsvs)
    cv2.imwrite("cropped_slides/%s.png" % file, correctedslide)
    outpath = "/home/skosaraju/%s/%s/%s/%s" % (project, stain,type,  file)
    path_extraction(correctedslide, outpath)
    return
def normal_regions(inputsvs,project,stain,type,file):
    print("yes")
    slide_dimensions, slide_img = reading_WSI(inputsvs)
    slide1 = np.asarray(slide_img, dtype="int32")
    outpath = "/home/skosaraju/%s/%s/%s/%s" % (project, stain,type,  file)
    path_extraction(slide1, outpath)
    return


def main(type):
    datapath = '/home/sharedstorage'
    project = 'CK_VS_HE'

    stain = 'CK'
    os.mkdir("/home/skosaraju/%s/%s/%s"%(project,stain,type))
    files = inputfolder('%s/%s/%s/%s'%(datapath,project,type,stain))
    for file in files:
        print(file)
        os.mkdir("/home/skosaraju/%s/%s/%s/%s"%(project,stain,type,file))
        inputsvs = '%s/%s/%s/%s/%s.svs'%(datapath,project,type,stain,file)

        print(type)
        if type == 'Normal':

            normal_regions(inputsvs, project, stain, type, file)
        else:
            inputxml = '%s/%s/%s/%s/%s.xml' % (datapath, project, type, stain, file)
            cancer_region_extraction(inputxml, inputsvs, project, stain,type,file)

    return

if __name__ == "__main__":
    main('Normal')
