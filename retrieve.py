#!/usr/bin/python

import RPi.GPIO as GPIO
import time

def main():
    #init gpio things
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(19,GPIO.OUT)

    #using -.3 row for claw servo
    pin_claw = GPIO.PWM(6,46.382)
    pin_step = GPIO.PWM(4,100)
    
    #for .5 seconds we open the claw
    print ("OPEN CLAAW")
    pin_claw.start(7.236)
    start_time = time.time()
    while (time.time() - start_time) <.2:
        time.sleep(.01)
    pin_claw.start(0)

    #for 2 seconds move the claw forward
    print("FORWARD")
    GPIO.output(19,0)
    pin_step.start(50)
    start_time = time.time()
    while (time.time() - start_time) <5:
        time.sleep(.01)
    pin_step.start(0)

    #for .8 seconds close the claw
    pin_claw.ChangeFrequency(46.642)
    pin_claw.start(6.716)
    start_time = time.time()
    while (time.time() - start_time) <1.2:
        time.sleep(.01)
    pin_claw.start(0)

    #for 2 seconds we withdraw the claw
    GPIO.output(19,1)
    pin_step.start(50)
    start_time = time.time()
    while (time.time() - start_time) <6:
        time.sleep(.01)
    pin_step.start(0)


    #Gpio cleanup to end the operation
    GPIO.cleanup()
