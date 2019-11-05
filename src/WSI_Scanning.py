import openslide
from openslide import (OpenSlide, OpenSlideError,OpenSlideUnsupportedFormatError)
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


def reading_WSI(slide_path):
    slide = OpenSlide(slide_path)
    slide_dimensions = slide.level_dimensions
    slide_img = slide.read_region((0, 0), 1, (slide.level_dimensions[1][0], slide.level_dimensions[1][1])).convert(
        'RGB')
    print(slide_dimensions, slide_img)
    return slide_dimensions, slide_img



def reading_WSI_with_annotations(slide_img, new_cordinate_list):
    # slide_dimensions, slide_img = reading_WSI(inputsvs)
    slide1 = np.asarray(slide_img, dtype="int32")

    out = np.zeros_like(slide1)
    for i in range(len(new_cordinate_list)):
        mask = np.zeros((slide1.shape[0], slide1.shape[1]))
        cv2.fillConvexPoly(mask, np.array(new_cordinate_list[i]), 1)
        mask = mask.astype(np.bool)

        out[mask] = slide1[mask]

        # out[out == [0,0,0]] =  [255,255,255]
        # cv2.imwrite("example.png",np.array(out))
    out = np.where(out != [0, 0, 0], out, [255,255,255])
    # print('yes')
    return np.array(out)