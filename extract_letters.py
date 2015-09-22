# import pyautogui as pg
import numpy as np
import colorsys
import cv2
import time
from PIL import Image, ImageOps, ImageEnhance
import pytesseract


image = cv2.imread("content/cards/b.png")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
_,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY) # threshold

# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
kernel = np.ones((2,2),np.uint8)
dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate

# cv2.imshow('image', dilated)
# cv2.waitKey(0)

contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

max_a = 40000
min_a = 2500

def check_bound(contour):
  [x,y,w,h] = cv2.boundingRect(contour)
  a = h*w
  return a < max_a and a > min_a

contours = filter(check_bound, contours)

# for each contour found, draw a rectangle around it on original image
for contour in contours:
  # get rectangle bounding contour
  [x,y,w,h] = cv2.boundingRect(contour)

  # draw rectangle around contour on original image
  # cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)

  # crop image for OCR
  cropped = gray[y-20:y+h+20, x-20:x+w+20]
  _,thresh_cropped = cv2.threshold(cropped,210,255,cv2.THRESH_BINARY) # threshold

  kernel = np.ones((2,2),np.uint8)
  dilated = cv2.dilate(thresh_cropped,kernel,iterations = 4) # dilate

  cv2.imshow('im', dilated)
  cv2.waitKey(0)

  pil_im = Image.fromarray(thresh_cropped)
  print 'Performing OCR...'
  print(pytesseract.image_to_string(pil_im))

# write original image with added contours to disk  
# cv2.imwrite("contoured.jpg", image) 
