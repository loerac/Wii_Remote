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
wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC

def d_pad(left_motor,right_motor):
    if left_motor != -1 or right_motor != -1:
        GPIO.output(EN_1,GPIO.HIGH)
        GPIO.output(EN_2,GPIO.HIGH)
        GPIO.output(DIR_1,left_motor)
        GPIO.output(DIR_2,right_motor)
    sleep(motor_stop)
    GPIO.output(EN_1, GPIO.LOW)
    GPIO.output(EN_2, GPIO.LOW)

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
        left_motor=-1
        right_motor=-1
        if(button & cwiid.BTN_LEFT):
            right_motor=1
        if(button & cwiid.BTN_RIGHT):
            left_motor=1
        if(button & cwiid.BTN_UP):
            right_motor=1
            left_motor=1
        if(button & cwiid.BTN_DOWN):
            right_motor=0
            left_motor=0
        d_pad(left_motor,right_motor)
    # Controlling the motors with the Accelerometer
    else:
        accel()
        if(button & cwiid.BTN_B):
            print("Calibrating: Please hold the Wii Remote still")
            #check= 0
            cali = 50
            acc_x_list = []
            acc_y_list = []
            acc_z_list = []
            while cali:
                temp = str(wii.state['acc'])
                acc = ""
                test = ""
                acc_x = 0
                acc_y = 0
                acc_z = 0
                for i in range(1, len(temp)):
                    if(temp[i]=='(' or temp[i]==',' or temp[i]==')' or temp[i]==' ' and acc!=''):
                        if(acc_x == 0):
                            acc_x = int(acc)
                            acc_x_list.append(acc_x)
                            test += "acc_x: %s" %(acc_x)
                        elif(acc_y == 0):
                            acc_y = int(acc)
                            acc_y_list.append(acc_y)
                            test += "  acc_y: %s" %(acc_y)
                        elif(acc_z == 0):
                            acc_z = int(acc)
                            acc_z_list.append(acc_z)
                            test += "  acc_z: %s" %(acc_z)
                        acc = ""
                    else:
                        acc += temp[i]
                sleep(0.01)
                #check = (button & cwiid.BTN_B)
                cali -= 1
                #print "RUN:",cali,test
            acc_x = 0
            acc_y = 0
            acc_z = 0
            cali = 50
            for i in range(0,(cali - 1)):
                acc_x += acc_x_list[i]
                acc_y += acc_y_list[i]
                acc_z += acc_z_list[i]
            sleep(delay)
            print "x:",acc_x / cali
            print "y:",acc_y / cali
            print "z:",acc_z / cali
            sleep(1)

def d_pad():
    if(button & cwiid.BTN_LEFT):
        print("LEFT")

        GPIO.output(EN_1, GPIO.HIGH)
        GPIO.output(EN_2, GPIO.HIGH)
        GPIO.output(DIR_1, False)
        GPIO.output(DIR_2, True)
    if(button & cwiid.BTN_RIGHT):
        print("RIGHT")
        GPIO.output(EN_1, GPIO.HIGH)
        GPIO.output(EN_2, GPIO.HIGH)
        GPIO.output(DIR_1, GPIO.HIGH)
        GPIO.output(DIR_2, GPIO.LOW)
    if(button & cwiid.BTN_UP):
        print("FORWARD")
        GPIO.output(EN_1, GPIO.HIGH)
        GPIO.output(EN_2, GPIO.HIGH)
        GPIO.output(DIR_1, GPIO.HIGH)
        GPIO.output(DIR_2, GPIO.HIGH)
    if(button & cwiid.BTN_DOWN):
        print("REVERSE")
        GPIO.output(EN_1, GPIO.HIGH)
        GPIO.output(EN_2, GPIO.HIGH)
        GPIO.output(DIR_1, GPIO.LOW)
        GPIO.output(DIR_2, GPIO.LOW)
    sleep(motor_stop)
    GPIO.output(EN_1, GPIO.LOW)
    GPIO.output(EN_2, GPIO.LOW)
