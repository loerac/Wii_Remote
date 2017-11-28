#!/usr/bin/python
#=========================================================================+
# Desc: A python script to utilize the Wii Remote with cwiid              |
#       The Wii remote will be controlling four DC motors with GPIO/PMod  |
# LED Indication: D-Pad[1] Accel[2] Connected[8]                          |
#=========================================================================+

# Libraries used
import cwiid
import RPi.GPIO as GPIO
from time import sleep

# Letting user know to press buttons on the Wii remote to connect
print"Press buttons 1 + 2 right now"
sleep(1)

# Attemp to connect to the wii remote
try:
    wii = cwiid.Wiimote()
except RuntimeError:
    print"Error opening wiimote connection"
    quit()

# Intialize variables 
delay = 0.25
mode = 1
motor_stop = 0.2

# Initialize motor control
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

print"Wii remote connected"
sleep(3)
wii.led = 9
print"Ready for use"

wii.rpt_mode = cwiid.RPT_BTN

while True:
    button = wii.state['buttons']

    # The [+] and [-] buttons are pressed at the same time exits program
    if(button - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        # Ensure motors are turned off
        GPIO.output(EN_1, GPIO.LOW)
        GPIO.output(EN_2, GPIO.LOW)
        print"It's time for royal rumble"
        wii.rumble = 1
        sleep(1)
        wii.rumble = 0
        exit(wii)

    # Choosing whether to control the motors using the
    # D-Pad by pressing button 1
    if(button & cwiid.BTN_1):
        mode = 1
        wii.led = 9
        print"D-Mode activated"
        sleep(delay)
    # Accelerometer by pressing button 2
    if(button & cwiid.BTN_2):
        mode = 2
        wii.led = 10
        print"Accelerometer activated"
        sleep(delay)

    # Controlling the motors with the D-Pad
    if(mode):
        GPIO.output(EN_1, GPIO.HIGH)
        GPIO.output(EN_2, GPIO.HIGH)

        if(button & cwiid.BTN_LEFT):
            GPIO.output(DIR_1, GPIO.LOW)
            GPIO.output(DIR_2, GPIO.HIGH)
        if(button & cwiid.BTN_RIGHT):
            GPIO.output(DIR_1, GPIO.HIGH)
            GPIO.output(DIR_2, GPIO.LOW)
        if(button & cwiid.BTN_UP):
            GPIO.output(DIR_1, GPIO.HIGH)
            GPIO.output(DIR_2, GPIO.HIGH)
        if(button & cwiid.BTN_DOWN):
            GPIO.output(DIR_1, GPIO.LOW)
            GPIO.output(DIR_2, GPIO.LOW)
        sleep(motor_stop)
        GPIO.output(EN_1, GPIO.LOW)
        GPIO.output(EN_2, GPIO.LOW)
    # Controlling the motors with the Accelerometer
    else:
        # A work on progress that'll be done by the end of the week
