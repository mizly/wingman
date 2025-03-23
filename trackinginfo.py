import cv2
import numpy as np


cap = cv2.VideoCapture(0)

while(1):

    _, frame = cap.read()
    #img = cv2.imread(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,120,70])
    upper_red = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)


    red_mask = cv2.bitwise_or(mask, mask2)

    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)  
        x, y, w, h = cv2.boundingRect(largest_contour) 
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 3) 
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
    




cv2.destroyAllWindows()
