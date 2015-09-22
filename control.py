# import pyautogui as pg
import numpy as np
import colorsys
# import cv2

# import time

from PIL import Image, ImageOps, ImageEnhance

import pytesseract

# failsafe - move mouse to top left to trigger abort
# pg.FAILSAFE = True

# screenWidth, screenHeight = pg.size()
# print screenWidth, screenHeight

# while True:
  # print pg.position()
  # pg.moveRel(None, 10)
  # pg.rightClick()

# screen = pg.screenshot()  # returns a Pillow/PIL Image object
# data = np.array(screen.getdata())
# print data.shape

# print np.reshape((), np.array(screen.getdata())).shape

  # print pg.locateOnScreen('snippet.png')

def threshold_pixels(p):
  if p < 200:
    return 255
  else:
    return 0

# print 'Loading image...'
# image = Image.open('abusive.png')
# enhancer = ImageEnhance.Contrast(image)

# factor = 5

# if image.mode == 'RGBA':
#   r,g,b,a = image.split()
#   rgb_image = Image.merge('RGB', (r,g,b))
#   # gray = rgb_image.convert('LA')

#   inverted_image = rgb_image

#   thresholded_img =  inverted_image.point(threshold_pixels)
#   # thresholded_img.save('thresholded_img.png')

#   binary_img = thresholded_img.convert('1')
#   binary_img.save('binary_img.png')
#   # enhancer = ImageEnhance.Contrast(inverted_gray)
#   # enhancer.enhance(factor).show("Sharpness %f" % factor)

#   # inverted_gray.save('invertedgray.png')

#   # r2,g2,b2 = inverted_image.split()
#   # final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
#   # final_transparent_image.save('new_file.png')
# else:
#   inverted_image = PIL.ImageOps.invert(img)
#   inverted_image.save('neww.png')

# print 'Performing OCR...'
# letters = Image.open('test.png')
# print(pytesseract.image_to_string(letters))



