import xml.etree.ElementTree as ET
from math import ceil
import random

import numpy as np
def parse(inputfile, regions, vertices):
    tree = ET.parse(inputfile)
    root = tree.getroot()

    # dictionary of point coordinates
    images = {}
    for region in root.iter(regions):
        coordinates = []
        for vertex in region.iter(vertices):
            temp = [int(i) for i in vertex.attrib.values()]
            coordinates.append(temp)

        # append the coordinates to images dictionary
        images.update({region.attrib["Id"]: np.array(coordinates)})

    return images


def annotation_conversion(slide_dimensions, coordinates):
    y_axis = slide_dimensions[1][1] / slide_dimensions[0][1]
    x_axis = slide_dimensions[1][0] / slide_dimensions[0][0]
    new_cordinate_list = []
    new_cordinate_list_temp = []
    # print(len(coordinates))

    for j in coordinates.values():
        coordinates_list = j
        new_cordinate_list_temp = []
        #     print(cent(j[0]*x_axis),cent(j[1]*y_axis,1))
        for k in range(len(coordinates_list)):
            #             print(k)
            new_cordinate_list_temp.append(
                (ceil(coordinates_list[k][0] * x_axis), ceil(coordinates_list[k][1] * y_axis)))
        new_cordinate_list.append(new_cordinate_list_temp)
    # print(len(new_cordinate_list))
    return new_cordinate_list

def eudlieandistance(A,B):
    d1 = (A[0]-B[0])**2
#     print(d1)
    d2 = (A[1]-B[1])**2
#     print(d2)
    d = np.sqrt(d1+d2)
    return d
def polygon_or_cross(cordinate_list):
    dist1 = eudlieandistance(cordinate_list[0],cordinate_list[-1])
    dist2 = eudlieandistance(cordinate_list[int(len(cordinate_list)/2)],cordinate_list[0])
    if dist2>dist1:
        return "polygen"
    else:
        return "cross"

def extracting_cancers_regions_annotations(inputfile,slide_dims):
    coordinates = parse(inputfile, regions='Region', vertices='Vertex')
    new_cordinate_list = annotation_conversion(slide_dims, coordinates)
    coordinate_filter_list = []
    for i in range(len(new_cordinate_list)):
        if polygon_or_cross(new_cordinate_list[i]) == "polygen":
            coordinate_filter_list.append(new_cordinate_list[i])
        else:
            None
    return coordinate_filter_list
