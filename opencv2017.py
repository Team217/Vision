# Team 217 ThunderChickens OpenCV Dual-Vision Code 2017
# By Robert J Dickens
# Developed for 2017 FIRST Robotics Compitition: FIRST Steamworks
# <3 Snowflake

# Import most recent versions of OpenCV-Python and NumPy for Python3.4
# Code has been confirmed to work in Python3.6, however Visual Studio does not support it
import cv2
import numpy as np

# Capture video from both camaras. First camara is 0, however using 1 and 2 is advised.
camA = cv2.VideoCapture(1)
camB = cv2.VideoCapture(2)

# Establish an infinite loop. Loop terminates when ESC is pressed.
while(1):
    k = 1
    
    # Process the video on a frame by frame basis.
    _, frameA = camA.read()
    _, frameB = camB.read()

    #Convert the BGR(full color) video into HSV(color data). This will allow us to break appart the image into seperate colors.
    hsvA = cv2.cvtColor(frameA, cv2.COLOR_BGR2HSV)
    hsvB = cv2.cvtColor(frameB, cv2.COLOR_BGR2HSV)

    # Define the range of color the HSV threshold will process. This color is a light-green, emitted by LED lights attached
    # to our robot. The light will reflect off Retro-Reflective Tape back to the vision cameras.
    lowerGreen = np.array([70,50,210])
    upperGreen = np.array([90,255,255])

    # Threshold the HSV
    maskA = cv2.inRange(hsvA, lowerGreen, upperGreen)
    maskB = cv2.inRange(hsvB, lowerGreen, upperGreen)

    # Use a Bitwise-AND method to super-impose the thresholded HSV (mask) onto the original image (frame)
    # This causes only green things to appear
    resA = cv2.bitwise_and(frameA, frameA, mask= maskA)
    resB = cv2.bitwise_and(frameB, frameB, mask= maskB)

    # Find contours in 'mask'. Contours are any significant change in color. In the mask, the colors are either
    # green or black, therefore any green will return as a contour.
    (_,cntrA,_) = cv2.findContours(maskA, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    (_,cntrB,_) = cv2.findContours(maskA, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # The 'max' function is used to find the largest contour on the 'mask'. If 'max' does not have
    # any values to return, it crashes the program. Therefore, the entirety of the code for processing
    # the contours into a bounding rectangle and returning the value of the center.
    try:
        finContA = max(cntrA, key = cv2.contourArea)

        x,y,w,h = cv2.boundingRect(finContA)
        cv2.rectangle(resA,(x,y),(x+w,y+h),(255,0,0),2)

        print("AX: ", (x+w/2))
        print("AY: ", (y+h/2))

    except:
        print('No Contours A')

    try:
        finContB = max(cntrB, key = cv2.contourArea)

        x2,y2,w2,h2 = cv2.boundingRect(finContB)
        cv2.rectangle(resB,(x2,y2),(x2+w2,y2+h2),(255,255,0),2)

        print("BX: ", (x2+w2/2))
        print("BY: ", (y2+h2/2))
    
    except:
        print('No Contours B')

    # For testing purposes, both the full color 'frame' and masked 'res' are displayed
    # through imshow. This will be unneccary during the event but helpful for testing certain colors.
    cv2.imshow('MASK ONE',resA)
    cv2.imshow('FULL COLOR ONE',frameA)
    cv2.imshow('MASK TWO',resB)
    cv2.imshow('FULL COLOR TWO',frameB)

    # Break the while statement once ESC (Key27) is pressed
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# Close everything
cv2.destroyAllWindows()