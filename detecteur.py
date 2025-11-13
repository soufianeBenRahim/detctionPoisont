import os
import sys
import time
import numpy as np
import cv2
import tkinter

#cap=cv2.VideoCapture(0)
cap=cv2.VideoCapture("poison2.mp4")
kernel_blur=5
seuil=15
surface=1000
center_coordinatesX = 300
center_coordinatesY = 300
radiuszone1=100
radiuszone2=200
radiuszone3=300
radiuszone4=400
ret, originale=cap.read()

Copyoriginale=originale.copy()
radius = 20
color = (255, 0, 0)
thickness = 2
def drawZones(preview) :
    cv2.circle(preview, (int(center_coordinatesX),int(center_coordinatesY)), 5, color, thickness)

    cv2.circle(preview, (int(center_coordinatesX),int(center_coordinatesY)), radiuszone1, color, thickness)
    cv2.circle(preview, (int(center_coordinatesX),int(center_coordinatesY)), radiuszone2, color, thickness)
    cv2.circle(preview, (int(center_coordinatesX),int(center_coordinatesY)), radiuszone3, color, thickness)
    result =cv2.circle(preview, (int(center_coordinatesX),int(center_coordinatesY)), radiuszone4, color, thickness)
    return result
def destance(x,y,a,b) :
    return pow((a-x), 2)+pow((b-y), 2)
def isPointInZone1(a,b) :
    destance=destance(center_coordinatesX,center_coordinatesY,a,b)
    return destance <= radiuszone1
def WhereZoneOfPoint(a,b) :
    destance=destance(center_coordinatesX,center_coordinatesY,a,b)
    if destance <= radiuszone1 :
        return 1
    if destance>radiuszone1 and destance<= radiuszone2 :
        return 2
    if destance>radiuszone2 and destance<= radiuszone3 :
        return 3
    if destance>radiuszone3 and destance<= radiuszone4 :
        return 4
    else :
        return 5
while True :
    originale=Copyoriginale.copy()
    cv2.imshow("original", drawZones(originale))
    key=cv2.waitKey(30)&0xFF
    if key==ord('q'):
        break
    if key==ord('s'):
        center_coordinatesX= center_coordinatesX-1
    if key==ord('d'):
        center_coordinatesX=center_coordinatesX+1
    if key==ord('e'):
        center_coordinatesY= center_coordinatesY-1
    if key==ord('x'):
        center_coordinatesY=center_coordinatesY+1
    if key==ord('f'):
        radiuszone1= radiuszone1+1 if radiuszone1+1<radiuszone2 else radiuszone1
    if key==ord('r'):
        radiuszone1=radiuszone1-1 if radiuszone1-1 >0 else radiuszone1
    if key==ord('g'):
        radiuszone2=radiuszone2+1 if radiuszone2+1<radiuszone3 else radiuszone2
    if key==ord('t'):
        radiuszone2=radiuszone2-1 if radiuszone2-1>radiuszone1 else radiuszone2
    if key==ord('h'):
        radiuszone3=radiuszone3+1 if radiuszone3+1<radiuszone4 else radiuszone3
    if key==ord('y'):
        radiuszone3=radiuszone3-1 if radiuszone3-1>radiuszone2 else radiuszone3
    if key==ord('j'):
        radiuszone4=radiuszone4+1
    if key==ord('u'):
        radiuszone4=radiuszone4-1 if radiuszone4-1>radiuszone3 else  radiuszone4
cv2.destroyAllWindows()

originale=cv2.cvtColor(originale, cv2.COLOR_BGR2GRAY)
originale=cv2.GaussianBlur(originale, (kernel_blur, kernel_blur), 0)
kernel_dilate=np.ones((5, 5), np.uint8)
while True:
    ret, frame=cap.read()
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray, (kernel_blur, kernel_blur), 0)
    mask=cv2.absdiff(originale, gray)
    mask=cv2.threshold(mask, seuil, 255, cv2.THRESH_BINARY)[1]
    mask=cv2.dilate(mask, kernel_dilate, iterations=3)
    contours, nada=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame_contour=frame.copy()
    nbContour=0
    sumX=0
    sumY=0
    centreMoyenn=(0,0)
    for c in contours:
        cv2.drawContours(frame_contour, [c], 0, (0, 255, 0), 5)
        if cv2.contourArea(c)<surface:
            continue
        x, y, w, h=cv2.boundingRect(c)
        nbContour=nbContour+1
        sumX=sumX+(x+w/2)
        sumY=sumY+(y+h/2)   
        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    if nbContour>0 :
        centrex=sumX/nbContour
        centrey=sumY/nbContour
        centreMoyenn=(int(centrex), int(centrey))  
        frame=cv2.circle(frame, centreMoyenn, 5, (0, 100, 100), thickness) 
    originale=gray
    frame=drawZones(frame)
    cv2.putText(frame, "[o|l]seuil: {:d}  [p|m]blur: {:d}  [i|k]surface: {:d}".format(seuil, kernel_blur, surface), (10, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 255), 2)
    cv2.imshow("frame", frame)
    #cv2.imshow("contour", frame_contour)
    #cv2.imshow("mask", mask)
    intrus=0
    key=cv2.waitKey(30)&0xFF
    if key==ord('q'):
        break
    if key==ord('p'):
        kernel_blur=min(43, kernel_blur+2)
    if key==ord('m'):
        kernel_blur=max(1, kernel_blur-2)
    if key==ord('i'):
        surface+=1000
    if key==ord('k'):
        surface=max(1000, surface-1000)
    if key==ord('o'):
        seuil=min(255, seuil+1)
    if key==ord('l'):
        seuil=max(1, seuil-1)

cap.release()
cv2.destroyAllWindows()
