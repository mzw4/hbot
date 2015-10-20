import pyautogui as pg
import numpy as np
import cv2
import time, itertools
from scipy.spatial import distance
from PIL import Image, ImageOps, ImageEnhance

# Custom modules
import util, ocr

# failsafe - move mouse to top left to trigger abort
pg.FAILSAFE = True

CONTENT_DIR = 'content/'

screenWidth, screenHeight = pg.size()
print screenWidth, screenHeight

CARD_WIDTH = 200
CARD_HEIGHT = 350

ENDTURN_IMAGE_COMPARISON_THRESHOLD = -4

class ScreenParser():
  def __init__(self):
    self.image_bank = {}
    self.load_images()

  def find_card_in_hand(self):
    print 'Finding card in hand...'
    screen = pg.screenshot()  # returns a Pillow/PIL Image object
    image = np.array(screen)
    image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)
    mx, my = pg.position()
    cropped = image[screenHeight/2 + 30 : screenHeight - 20,\
                    mx - CARD_WIDTH*0.8: mx + CARD_WIDTH*0.8]
    # cropped = image[my - CARD_HEIGHT : my,\
    #                 mx - CARD_WIDTH*0.8: mx + CARD_WIDTH*0.8]

    # pos = ocr.locate_card_in_image(cropped)
    return cropped

  def load_images(self):
    # load endturn
    self.image_bank['endturn'] = cv2.imread(CONTENT_DIR + 'endturn.png', cv2.IMREAD_COLOR)
    # load green endturn
    self.image_bank['endturn_green'] = cv2.imread(CONTENT_DIR + 'endturn_green.png', cv2.IMREAD_COLOR)
    # load enemy turn
    self.image_bank['enemyturn'] = cv2.imread(CONTENT_DIR + 'enemyturn.png', cv2.IMREAD_COLOR)
    # load VS
    # image_bank['vs'] = cv2.imread(CONTENT_DIR + 'vs.png')
    # load play
    self.image_bank['play'] = cv2.imread(CONTENT_DIR + 'play.png', cv2.IMREAD_COLOR)
    # load play game
    self.image_bank['playgame'] = cv2.imread(CONTENT_DIR + 'playgame.png', cv2.IMREAD_COLOR)
    # load click to continue
    self.image_bank['continue'] = cv2.imread(CONTENT_DIR + 'continue.png', cv2.IMREAD_COLOR)

  """
  Check if it's the player's turn, return True if yes
  """
  def check_turn(self):
    print 'Checking turn...'
    # compare current turn indicator with image
    shot = util.screen_end_turn()
    cv2.imwrite('temp/screenturn.png', shot)
    enemyturn_dist = self.compareImages(shot.copy(), self.image_bank['enemyturn'])
    endturn_dist = self.compareImages(shot.copy(), self.image_bank['endturn'])
    print 'Distances %f %f' % (endturn_dist, enemyturn_dist)
    return abs(endturn_dist) < abs(enemyturn_dist)

  def compareImages(self, img1, img2):
    print 'Comparing images...'
    gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) # grayscale
    gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY) # grayscale
    _,thresh1 = cv2.threshold(gray1,150,255,cv2.THRESH_BINARY) # threshold
    _,thresh2 = cv2.threshold(gray2,150,255,cv2.THRESH_BINARY) # threshold
    cv2.imwrite('temp/turncheck_thresh1.png', thresh1)
    cv2.imwrite('temp/turncheck_thresh2.png', thresh2)
    print sum(thresh1.flatten()), sum(thresh2.flatten())
    return distance.euclidean(thresh1.flatten(), thresh2.flatten())

# sp = ScreenParser()
# sp.check_turn()
# sp.find_card_in_hand()












# ====================== Legacy ======================

# while True:
  # print pg.position()
  # pg.moveRel(None, 10)
  # pg.rightClick()


# print np.reshape((), np.array(screen.getdata())).shape

  # print pg.locateOnScreen('snippet.png')

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



