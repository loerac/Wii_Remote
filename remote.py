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
forward = {}
reverse = {}
left = {}
right = {}

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
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

# Deciding which direction to move the motors
def motor_out(left_motor,right_motor):
    if left_motor != -1 and right_motor != -1:
        GPIO.output(EN_1,GPIO.HIGH)
        GPIO.output(EN_2,GPIO.HIGH)
        GPIO.output(DIR_1,left_motor)
        GPIO.output(DIR_2,right_motor)
    sleep(motor_stop)
    GPIO.output(EN_1, GPIO.LOW)
    GPIO.output(EN_2, GPIO.LOW)

def accel():
    acc_x = 0
    acc_y = 0
    # Will give a string value with '(', ',', ')' and ' '
    axis = str(wii.state['acc'])
    acc = ""
    for i in range(1,len(axis)):
        # Get the value of the accelerometer of x, y, z without the other characters
        if(axis[i]=='(' or axis[i]==',' or axis[i]==')' or axis[i]==' ' and acc!=''):
            if(acc_x == 0):
                acc_x = int(acc)
            elif(acc_y == 0):
                acc_y = int(acc)
            else:
                return acc_x,acc_y,int(acc)
            acc = ""
        else:
            acc += axis[i]
    return 0,0,0

def calibrate():
    cal = 100
    pos = ['FORWARD', 'REVERSE', 'LEFT', 'RIGHT']
    for i in range(len(pos)):
        acc_x = 0
        acc_y = 0
        acc_z = 0
        print "Tilt Wii Remote to :",pos[i], "position"
        sleep(3)
        while cal:
            # Get an average reading on the current state of the remote
            x,y,z = accel()
            acc_x += x
            acc_y += y
            acc_z += z
            sleep(0.01)
            cal -= 1
        cal = 100

        # Set the keys to a value in the dictionary
        if pos[i] == 'FORWARD':
            forward['x'] = (acc_x / cal)
            forward['y'] = (acc_y / cal)
            forward['z'] = (acc_z / cal)
            print "FORWARD DICT:",forward
        elif pos[i] == 'REVERSE':
            reverse['x'] = (acc_x / cal)
            reverse['y'] = (acc_y / cal)
            reverse['z'] = (acc_z / cal)
            print "REVERSE DICT:",reverse
        elif pos[i] == 'LEFT':
            left['x'] = (acc_x / cal)
            left['y'] = (acc_y / cal)
            left['z'] = (acc_z / cal)
            print "LEFT DICT:",left
        elif pos[i] == 'RIGHT':
            right['x'] = (acc_x / cal)
            right['y'] = (acc_y / cal)
            right['z'] = (acc_z / cal)
            print "RIGHT DICT:",right

while True:
    button = wii.state['buttons']

    # The [+] and [-] buttons are pressed at the same time exits program
    if(button - cwiid.BTN_PLUS - cwiid.BTN_MINUS == 0):
        # Ensure motors are turned off
        GPIO.output(EN_1, GPIO.LOW)
        GPIO.output(EN_2, GPIO.LOW)
        print"It's time for royal rumble"
        wii.rumble = 1
        sleep(0.5)
        wii.rumble = 0
        exit(wii)

    # Choosing whether to control the motors using the
    # D-Pad by pressing button 1
    if(button & cwiid.BTN_1):
        GPIO.output(EN_1, GPIO.LOW)
        GPIO.output(EN_2, GPIO.LOW)
        mode = 1
        wii.led = 9
        print"D-Mode activated"
        sleep(delay)
    # Accelerometer by pressing button 2
    if(button & cwiid.BTN_2):
        mode = 0
        wii.led = 10
        print"Accelerometer activated"
        sleep(delay)

    # Controlling the motors with the D-Pad
    if(mode):
        if(button & cwiid.BTN_LEFT):
            print("LEFT")
            motor_out(0,1)
        if(button & cwiid.BTN_RIGHT):
            print("RIGHT")
            motor_out(1,0)
        if(button & cwiid.BTN_UP):
            print("FORWARD")
            motor_out(1,1)
        if(button & cwiid.BTN_DOWN):
            print("REVERSE")
            motor_out(0,0)
    # Controlling the motors with the Accelerometer
    else:
        if(button & cwiid.BTN_B or (not bool(forward))):
            print("\n\nCalibrating: Please hold the Wii Remote still")
            calibrate()
            print("\n\nDone calibrating")
            print("3")
            sleep(1)
            print("2")
            sleep(1)
            print("1")
            sleep(1)
            print("KA-CHOW")

        # Brakes while using the accelerometer
        if(button & cwiid.BTN_A):
            GPIO.output(EN_1, GPIO.LOW)
            GPIO.output(EN_2, GPIO.LOW)
            print("E-BRAKES ACTIVATED")
        else:
            GPIO.output(EN_1, GPIO.HIGH)
            GPIO.output(EN_2, GPIO.HIGH)

            # Get current reading values from the accelerometer
            acc_x,acc_y,acc_z = accel()
            diff = 7

            # Decide which direction to move
            if((acc_x < (int(forward['x']) + diff)) and (acc_x > (int(forward['x']) - diff))):
                if((acc_y < (int(forward['y']) + diff)) and (acc_y > (int(forward['y']) - diff))):
                    if((acc_z < (int(forward['z']) + diff)) and (acc_z > (int(forward['z']) - diff))):
                        print("FORWARD")
                        motor_out(1,1)
            elif((acc_x < (int(reverse['x']) + diff)) and (acc_x > (int(reverse['x']) - diff))):
                if((acc_y < (int(reverse['y']) + diff)) and (acc_y > (int(reverse['y']) - diff))):
                    if((acc_z < (int(reverse['z']) + diff)) and (acc_z > (int(reverse['z']) - diff))):
                        print("REVERSE")
                        motor_out(0,0)
            elif((acc_x < (int(left['x']) + diff)) and (acc_x > (int(left['x']) - diff))):
                if((acc_y < (int(left['y']) + diff)) and (acc_y > (int(left['y']) - diff))):
                    if((acc_z < (int(left['z']) + diff)) and (acc_z > (int(left['z']) - diff))):
                        print("LEFT")
                        motor_out(0,1)
            elif((acc_x < (int(right['x']) + diff)) and (acc_x > (int(right['x']) - diff))):
                if((acc_y < (int(right['y']) + diff)) and (acc_y > (int(right['y']) - diff))):
                    if((acc_z < (int(right['z']) + diff)) and (acc_z > (int(right['z']) - diff))):
                        print("RIGHT")
                        motor_out(1,0)
            # Stop moving if none of the directions fit
            else:
                print("STATIONARY")
                GPIO.output(EN_1, GPIO.LOW)
                GPIO.output(EN_2, GPIO.LOW)
