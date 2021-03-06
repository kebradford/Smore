#!/usr/bin/python

#this is a script to read in camera data of a detected marshmallow, and read it's toastedness
#toastedness will be done via averaging pixel data of detected marshmallow shape
#script also rotates the toasting stepper and 
#TODO
#controls heating element activation

import sys
import cv2
import numpy as np
import imutils
import RPi.GPIO as GPIO
import time 

#basic color definitions
RED = (255,0,0)
WHITE = (255,255,255)

#contour that is the mallow
Mallow_Cont = []
#desired toastedness of the mallow
Toast_Level = 0

#average array
Avg_Toast = []
start_toast = 255
Index = 0

#this function takes in a grayscale image and a given contour to find
#the darkening of the specific region bound by the contour
def RoastLevel(img):

    global Mallow_Cont
    global Avg_Toast
    global Index
    global start_toast
    c = Mallow_Cont
    
    #finding the pixels in a given contour and creating a mask of those pixels
    mask = np.zeros_like(img)
    cv2.drawContours(mask, c,-1, color=255,thickness =-1)

    #recording the pixels on the interior of the mask
    pixs = np.where(mask==255)

    #initialize several useful variables
    pix_dark = 0    #total darkness value of the region
    count = 0       #number of pixels counted
    roast_level = 0 #overall roast level

    #ensuring that there are some interior pixels
    if(len(pixs[0]) > 0):

        #working through all interior pixels
        for i in range(len(pixs[0])):
        
            #summing up the grayscale value for level of "darkening
            pix_dark += img[pixs[0][i],pixs[1][i]]
            count +=1

        #final calculation of darkness
        roast_level = pix_dark/float(count)
        if  len(Avg_Toast) is 0:
            Avg_Toast = [roast_level] * 12
            start_toast = sum(Avg_Toast)/len(Avg_Toast)
            print("starting roast level is")
            print(start_toast)
            Index = 0
        else:
            Avg_Toast[Index] = roast_level
            Index = Index + 1
            Index = Index % 12
    
    return sum(Avg_Toast)/len(Avg_Toast)


def main(TL,C):

    #global
    global Mallow_Cont
    global Toast_level
    global start_toast
    
    Mallow_Cont = C
    Toast_Level = TL
    #setting up GPIO to turn mallow
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)


    pin = GPIO.PWM(5,46.554)


    #basic video capture object
    videoCap = cv2.VideoCapture(0)

    #checking successful video capture creation
    if(not videoCap.isOpened()):
        print ("ERROR CANT FIND PI CAMERA")
        quit()
    else:
        print("camera found")


    #reading in an initial frame
    b, image = videoCap.read()
    
    #starting the rotating of skewer
    
    pin.start(6.89)
    
    #the roast level of mallow (255 white 0 black)
    roastLevel = 255
    start_toast = 255
    #converting toast level to darkness value
    cookLevel = 20 +  Toast_Level*5
    print("Cook Level is")
    print (cookLevel)
    time_start = time.time() 
    init = True

    while roastLevel - start_toast < cookLevel :
        if(time.time()-time_start > .2 or init is True):
            time_start = time.time()
            init = False
            #reading in a frame
            b, image = videoCap.read()

            #adjusting for more processing
            #im_resize = imutils.resize(image, width=300)
            #ratio = image.shape[0]/float(im_resize.shape[0])
            image = imutils.resize(image, width = 320, height =240)
            image = image[70:220, 70:200]
            #image processing steps
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  #grayscale

        
            #displaying the toastedness level of the desired contour
            #location of printing
            c_x = 50 
            c_y = 75
        
            #draw contour 
            cv2.drawContours(image, [Mallow_Cont], -1, RED,-1)
            cv2.putText(image, "Roast_Level", (c_x,c_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)
        
            #displaying the associated toastedness
            roastLevel = RoastLevel(gray)
            cv2.putText(image, str(roastLevel), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 2)


            cv2.imshow("Gray", gray)
            cv2.imshow("Image", image)
            cv2.waitKey(1)
    print("final roast level is:")
    print (roastLevel)
    pin.ChangeDutyCycle(0)
    GPIO.cleanup()
