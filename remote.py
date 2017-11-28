#!/usr/bin/python

import cwiid
import RPi.GPIO as GPIO
from time import sleep

print"Press buttons 1 + 2 right now"
sleep(1)

delay = 0.25
mode = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
EN_1 = 18
EN_2 = 17
DIR_1 = 23
DIR_2 = 22

GPIO.setup(EN_1, GPIO.OUT)
GPIO.setup(EN_2, GPIO.OUT)
GPIO.setup(DIR_1, GPIO.OUT)
GPIO.setup(DIR_2, GPIO.OUT)
sleep(1)

# Attemp to connect to the wii remote
try:
    wii = cwiid.Wiimote()
except RuntimeError:
    print"Error opening wiimote connection"
    quit()

print"Wii remote connected"
sleep(3)
wii.led = 9
print"Ready for use"

wii.rpt_mode = cwiid.RPT_BTN

while True:
    button = wii.state['buttons']
    
    if(button - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        GPIO.output(EN_1, GPIO.LOW)
        GPIO.output(EN_2, GPIO.LOW)
        print"It's time for royal rumble"
        wii.rumble = 1
        sleep(1)
        wii.rumble = 0
        exit(wii)

    if(button & cwiid.BTN_1):
        mode = 1
        wii.led = 9
        print"D-Mode activated"
        sleep(delay)
    if(button & cwiid.BTN_2):
        mode = 2
        wii.led = 10
        print"Accelerometer activated"
        sleep(delay)

    if(mode):
        brk = 0.2 
        if(button & cwiid.BTN_LEFT):
            GPIO.output(EN_1, GPIO.HIGH)
            GPIO.output(EN_2, GPIO.HIGH)
            GPIO.output(DIR_1, GPIO.LOW)
            GPIO.output(DIR_2, GPIO.HIGH)
        if(button & cwiid.BTN_RIGHT):
            GPIO.output(EN_1, GPIO.HIGH)
            GPIO.output(EN_2, GPIO.HIGH)
            GPIO.output(DIR_1, GPIO.HIGH)
            GPIO.output(DIR_2, GPIO.LOW)
        if(button & cwiid.BTN_UP):
            GPIO.output(EN_1, GPIO.HIGH)
            GPIO.output(EN_2, GPIO.HIGH)
            GPIO.output(DIR_1, GPIO.HIGH)
            GPIO.output(DIR_2, GPIO.HIGH)
        if(button & cwiid.BTN_DOWN):
            GPIO.output(EN_1, GPIO.HIGH)
            GPIO.output(EN_2, GPIO.HIGH)
            GPIO.output(DIR_1, GPIO.LOW)
            GPIO.output(DIR_2, GPIO.LOW)
        sleep(brk)
        GPIO.output(EN_1, GPIO.LOW)
        GPIO.output(EN_2, GPIO.LOW)
