import math
import numpy as np
import cv2
import pyautogui as pg

# import matplotlib.pyplot as plt

def screenshot(x, y, w, h):
  image = np.array(pg.screenshot())
  image = cv2.cvtColor(image, cv2.cv.CV_BGR2RGB)
  return image[y:y+h, x:x+w]

def screen_end_turn():
  screenWidth, screenHeight = pg.size()
  shot = screenshot(screenWidth/2 + 470 - 60, screenHeight/2 - 25 - 25, 120, 60)
  return shot

def screen_end_turn_save():
  screenWidth, screenHeight = pg.size()
  shot = screenshot(screenWidth/2 + 470 - 60, screenHeight/2 - 25 - 25, 120, 60)
  cv2.imwrite('content/endturn.png', shot)

def get_y_circle(x, radius, centerX, centerY):
  return -math.sqrt(radius**2 - (x - centerX)**2) + centerY

# screen_end_turn_save()

# xs = range(0, 100)
# ys = []
# for x in xs:
#   ys += [get_y_circle(x, 50, 50, 0)]

# plt.xlim((0, 100))
# plt.ylim((-50, 50))
# plt.plot(xs, ys)
# plt.show()