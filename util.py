import numpy as np
import cv2
import pyautogui as pg

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


# screen_end_turn_save()


