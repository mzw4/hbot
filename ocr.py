# import pyautogui as pg
import numpy as np
import colorsys
import cv2
import time
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

test_path = "content/cards/mog.png"
max_a = 40000
min_a = 2500

def detect_letter(contour):
  # check for too many consecutive same-y pixels
  ycount = 0
  prevy = None
  for pt in contour:
    if pt[0][0] == prevy:
      ycount += 1
    prevy = pt[0][0]
  return ycount < 20

def filter_contours(image):
  kernel = np.ones((2,2),np.uint8)
  dilated = cv2.dilate(image,kernel, iterations = 1) # dilate

  contours, hierarchy = cv2.findContours(dilated.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
  for c in contours:
    [x,y,w,h] = cv2.boundingRect(c)
    # print x,y,w,h

    if w > 20 and h < 10 or h*w < 100 and h < 10:
      for i in range(y, y+h):
        for j in range(x, x+w):
          image[i, j] = 0

      # for pt in c:
      #   (px, py) = pt[0]
      #   image[py, px] = 0

      dilated2 = cv2.cvtColor(dilated,cv2.COLOR_GRAY2BGR) # grayscale
      cv2.rectangle(dilated2,(x,y),(x+w,y+h),(255,0,255),1)
      # cv2.imshow('im', dilated2)
      # cv2.waitKey(0)

    # else:
      # print detect_letter(contour)

  return image

def check_bound(contour):
  [x,y,w,h] = cv2.boundingRect(contour)
  a = h*w
  return a < max_a and a > min_a

def perform_ocr(path):
  image = cv2.imread(path)

  # process the image
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
  _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY) # threshold
  # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
  kernel = np.ones((2,2),np.uint8)
  dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate

  # cv2.imshow('image', dilated)
  # cv2.waitKey(0)

  # find the contours of the image and filter according to bounding boxes
  # look for the text in the center of the card
  contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
  contours = filter(check_bound, contours)

  if len(contours) > 1 or not contours:
    return

  # get rectangle bounding contour
  [x,y,w,h] = cv2.boundingRect(contours[0])

  # draw rectangle around contour on original image
  # cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)

  # crop image for OCR
  cropped = gray[y-5:y+h+5, x-5:x+w+5]
  _,thresh_cropped = cv2.threshold(cropped,210,255,cv2.THRESH_BINARY) # threshold

  filtered = filter_contours(thresh_cropped.copy())

  # kernel = np.ones((2,2),np.uint8)
  # filtered = cv2.dilate(filtered,kernel, iterations = 1) # dilate

  # cv2.imshow('im', (255-filtered))
  # cv2.waitKey(0)

  pil_im = Image.fromarray((255-filtered))
  print 'Performing OCR...'
  return pytesseract.image_to_string(pil_im)


# perform_ocr(test_path)


