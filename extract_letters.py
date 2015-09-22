# import pyautogui as pg
import numpy as np
import colorsys
import cv2
import time
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

def makewhite(p):
  return 0

# mask = Image.open('abusive.png').point(makewhite)
# mask = mask.convert("L")


# image = Image.open('abusive.png')
# image.putalpha(mask)

image = cv2.imread("abusive.png")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
_,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY) # threshold

# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
kernel = np.ones((2,2),np.uint8)
dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate

cv2.imshow('image', dilated)
cv2.waitKey(0)

contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours

# for each contour found, draw a rectangle around it on original image
for contour in contours:
  # get rectangle bounding contour
  [x,y,w,h] = cv2.boundingRect(contour)
  a = h*w

  print [x,y,w,h]
  # discard areas that are too large
  if a > 40000:
      continue

  # discard areas that are too small
  if a < 2500:
      continue

  # draw rectangle around contour on original image
  cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)

# write original image with added contours to disk  
cv2.imwrite("contoured.jpg", image) 





def threshold_pixels(p):
  if p < 200:
    return 255
  else:
    return 0

def bfs_black(pixels):
  searched = np.zeros(pixels.shape)



# image = image.point(threshold_pixels).convert('1')
# w, h = image.size

# pixels = np.reshape(np.array(image.getdata()), (w, h))

# bfs_black(pixels)