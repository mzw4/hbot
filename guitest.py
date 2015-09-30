import pyautogui as pg

# pg.dragRel(None, -500)
test_path = "errors/error4.png"
image = cv2.imread(test_path)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # grayscale
_,thresh = cv2.threshold(gray,250,255,cv2.THRESH_BINARY) # threshold
# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
kernel = np.ones((2,2),np.uint8)
dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate

