import cv2
import numpy as np
from networktables import NetworkTable
import logging
logging.basicConfig(level=logging.DEBUG)

# network table setup
NetworkTable.setIPAddress("10.2.17.2")#127.0.0.1 with tester program
NetworkTable.setClientMode()
NetworkTable.initialize()
sd = NetworkTable.getTable("SmartDashboard")

# VideoCapture webcam id=0,1,2,3...
vc = cv2.VideoCapture(0)

# try to get the first frame
if vc.isOpened():
    rval, src = vc.read()
else:
    rval = False

def nothing(x):
    pass
cv2.namedWindow('image')


#Loop to process video
while rval:
    #value to alter
    thrval = 120 

    rval, src = vc.read()#camera feed
    #src = cv2.imread("C:/Users/stephen/Desktop/TC/2016/Grip/RealFullField/RealFullField/278.jpg")#image file

    # convert the image to grayscale and threshold it
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray",gray)
    ret,thr = cv2.threshold(gray,thrval,255,0)
    cv2.imshow("thr",thr)

    try:
    # find the contours and keep the largest one
        (_,cnts, _) = cv2.findContours(thr, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        c = max(cnts,key = cv2.contourArea, default=1)   # draw bounding recangle
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(src,(x,y),(x+w,y+h),(0,255,0),2)
    except:
        print('oops')
    #dislay var
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(src,'cogx: '+str(x +w/2),(10,50), font, .75,(0,255,0),2,cv2.LINE_AA)
    cv2.putText(src,'cogy: '+str(y+h/2),(10,80), font, .75,(0,255,0),2,cv2.LINE_AA)

    # send to network tables
    print('SendingX... ', (x+w/2))
    sd.putNumber('COG_X', (x+w/2))
    print('SendingY... ', (y+h/2))
    sd.putNumber('COG_Y', (y+h/2))
    
    # display image
    cv2.imshow("src", src)

    # escape key: ESC
    key = cv2.waitKey(20)
    if key == 27: 
        break

# close the window and releases camera
cv2.destroyAllWindows()
vc.release()

