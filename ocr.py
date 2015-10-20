# import pyautogui as pg
import numpy as np
import cv2
import time
from PIL import Image, ImageOps, ImageEnhance
import pytesseract

# test_path = "content/cards/pow.png"
test_path = "temp/original_defense_image.png"
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

def check_bound(w, h):
  a = h*w
  return a < max_a and a > min_a and w > 150

def process_image(image):
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
  _,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY) # threshold
  # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
  kernel = np.ones((2,2),np.uint8)
  dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate

  print 'Saving pics'
  cv2.imwrite('temp/process_dilated.png', dilated)
  cv2.imwrite('temp/process_thresh.png', thresh)
  cv2.imwrite('temp/process_gray.png', gray)
  cv2.imwrite('temp/process_image.png', image)

  # find the contours of the image and filter according to bounding boxes
  # look for the text in the center of the card
  # pick contour with max width to identify the card name text
  contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
  return contours, gray

"""
Return the larger of the two bounds
"""
def filter_bound_get_max(box1, box2):
  [x,y,w,h] = box1
  [x2,y2,w2,h2] = box2

  in_bound1 = check_bound(w, h)
  in_bound2 = check_bound(w2, h2)
  
  if not in_bound1: return box2
  elif not in_bound2: return box1
  elif w > w2: return box1

"""
Remove irrelevant contours segments from image
"""
def filter_contours(image):
  kernel = np.ones((2,2),np.uint8)
  dilated = cv2.dilate(image,kernel, iterations = 1) # dilate

  cv2.imwrite('temp/before_filter_cropped_image.png', image)

  contours, hierarchy = cv2.findContours(dilated.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
  for c in contours:
    [x,y,w,h] = cv2.boundingRect(c)

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

  cv2.imwrite('temp/filtered_cropped_image.png', dilated)
  return image

"""
Perform the OCR
"""
def perform_ocr(image):
  contours, gray = process_image(image)

  bounding_boxes = map(lambda c: cv2.boundingRect(c), contours)
  if not bounding_boxes:
    print 'No contours!'
    return

  # get rectangle bounding card name contour
  [x,y,w,h] = reduce(filter_bound_get_max, bounding_boxes)

  # draw rectangle around contour on original image
  # cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,255),2)

  # crop image for OCR
  (ih, iw) = gray.shape
  cropped = gray[max(y-5,0):min(y+h+5,ih), max(x-5,0) : min(x+w+5, iw)]

  # threshold and filter contours
  _,thresh_cropped = cv2.threshold(cropped,210,255,cv2.THRESH_BINARY) # threshold
  filtered = filter_contours(thresh_cropped.copy())

  # kernel = np.ones((2,2),np.uint8)
  # filtered = cv2.dilate(filtered,kernel, iterations = 1) # dilate

  pil_im = Image.fromarray((255-filtered))
  pil_im.save('temp/ocr_image2.png')

  print 'Performing OCR...'
  result = pytesseract.image_to_string(pil_im)
  print result + '!'
  return result

  # return pytesseract.image_to_string(pil_im)

"""
Return the position of a card in the image, if possible
"""
def locate_card_in_image(image):
  contours, gray = process_image(image)
  for c in contours:
    # look for the top left number to identify a card
    [x,y,w,h] = cv2.boundingRect(c)
    print x, y, w, h
    if w > 20 and h > 50 and w < 70 and h < 70 and w * h > 1000 and w * h < 5000:
        print 'Returning!'
        return x, y
  return None




image = cv2.imread(test_path)
print perform_ocr(image)
