import imutils
import matplotlib.pyplot as plt
import cv2
import numpy as np
from tkinter import *
from skimage import filters,exposure
from PIL import Image, ImageStat
import matplotlib.pyplot as plt
from skimage.morphology import disk
from matplotlib.font_manager import FontProperties
global screenCnt
import functools

def preProcess(p):
    ratio = p.shape[0] / 800.0  # scale the image
    p = imutils.resize(p, height=800)

    grayImage  = cv2.cvtColor(p, cv2.COLOR_BGR2GRAY)  # get the gray image
    # before we do the canny edge detection, we need to use the gaussian blur to reduce the noise
    # otherwise we cannot detect the edge successfully
    gaussImage = cv2.GaussianBlur(grayImage, (5, 5), 0)
    edgedImage = cv2.Canny(gaussImage, 75, 200)  # 75 and 200 are the thresholds
    
    # contour retrieval mode: Retrieve all the outlines and put them in the list,
    # contour approximation method: only retain end points, save memory
    cnts = cv2.findContours(edgedImage.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # for different version the location of the Contour list is different
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    # sort the contours according to the area (i.e. size) from largest to smallest
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]
    screenCnt = [0]
    for c in cnts:
        # to see whether shape is a closed contour (if passed True), or just a curve.
        peri = cv2.arcLength(c, True)  # Calculating contour circumference
        # approximate the shape, parameter at 10%
        approx = cv2.approxPolyDP(c, 0.1 * peri, True)
        # if we find the edge correctly, return the value approx
        # else we didn't find the correct edge, return 0
        if len(approx) == 4:
            screenCnt = approx
            break
        else:
            screenCnt = [0]
            break

    return screenCnt, ratio

def order_points(pts):
    rect = np.zeros((4,2), dtype = "float32")

    s = np.sum(pts, axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def m_filter(img,x, y, step):
    # Empty Array
    sum_s=[] 
    for k in range(-int(step/2),int(step/2)+1):
        for m in range(-int(step/2),int(step/2)+1):
            sum_s.append(img[x+k][y+m])
    # Sort from small to big
    sum_s.sort()
    return sum_s[(int(step*step/2)+1)]

def transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.sqrt((tr[0] - tl[0]) ** 2 + (tr[1] - tl[1]) ** 2)
    widthB = np.sqrt((br[0] - bl[0]) ** 2 + (br[1] - bl[1]) ** 2)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt((tr[0] - br[0]) ** 2 + (tr[1] - br[1]) ** 2)
    heightB = np.sqrt((tl[0] - bl[0]) ** 2 + (tl[1] - bl[1]) ** 2)
    maxHeight = max(int(heightA), int(heightB))

    dst = np.array([
        [0,0],
        [maxWidth - 1, 0],
        [maxWidth -1, maxHeight -1],
        [0, maxHeight -1]], dtype = "float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    transformed = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return transformed

def Contrast_and_Brightness(alpha,beta,img):
    #f(x)=Ag(x)+B
    #A Adjust Contrast, B Adjust Brightness
    #Zeros
    blank = np.zeros(img.shape,img.dtype)
    #Add Weight
    dst = cv2.addWeighted(img,alpha,blank,1-alpha,beta)
    return dst

def detect_color_image(file):
    COLOR = 100
    v = ImageStat.Stat(Image.open(file)).var
    if len(v) == 3:
        maxmin = abs(max(v) - min(v))
        if maxmin > COLOR:
            return 1
        else:
            return 2



