import cv2
import numpy as np


cap = cv2.VideoCapture(0)

# Blue Green Red
penColorHSV = [[78, 144, 12, 137, 255, 162],
               [67, 83, 65, 95, 214, 96],
               [0, 107, 114, 179, 237, 216]]

# colors of pen tips
penColorBGR = [[255, 0, 0], 
               [0, 255, 0],
               [0, 0, 255]]

# record positions and color of every pen
# [x, y, colorId(0:B; 1:G; 2:R)]
drawPoints = []


def findPen(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # change BGR to HSV
    
    # find every color
    for i in range(len(penColorHSV)):
        lower = np.array(penColorHSV[i][:3])  
        upper = np.array(penColorHSV[i][3:6])  
        
        mask = cv2.inRange(hsv, lower, upper)  # filter the color
        result = cv2.bitwise_and(img, img, mask=mask)  # use mask to get the right color
        penx, peny = findContour(mask)
        cv2.circle(imgContour, (penx, peny), 10, penColorBGR[i], cv2.FILLED)
        
        # check whether it find the contour
        if peny != -1:  
            drawPoints.append([penx, peny, i])
        cv2.imshow('result', result)
    
def findContour(img):
    # find the shape of the pen
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    x, y, w, h = -1, -1, -1, -1
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            vertices = cv2.approxPolyDP(cnt, peri * 0.02, True)  # speculate which shape 
            x, y, w, h = cv2.boundingRect(vertices)  # frame 
    
    # return the spot of pen tip   
    return x+w//4, y   


def draw(drawpoints):
    for point in drawpoints:
        cv2.circle(imgContour, (point[0], point[1]), 10, penColorBGR[point[2]], cv2.FILLED)
        
while True:
    ret, frame = cap.read()
    if ret:
        imgContour = frame.copy()
        cv2.imshow('video', frame)
        findPen(frame)
        draw(drawPoints)
        cv2.imshow('contour', imgContour)
    else:
        break
    if cv2.waitKey(1) == ord('h'):
        break 
    
