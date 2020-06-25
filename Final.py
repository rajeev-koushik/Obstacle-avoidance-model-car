import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 18
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(12,GPIO.OUT)
p=GPIO.PWM(12,50)
p.start(7.5)

GPIO.setup(17,GPIO.OUT)#Buzzer
GPIO.output(17,False)
GPIO.setup(22,GPIO.IN) #Proximity Sensor

from gpiozero import PWMOutputDevice
from gpiozero import DigitalOutputDevice
from time import sleep
 
#///////////////// Define Motor Driver GPIO Pins /////////////////
# Motor A, Left Side GPIO CONSTANTS
PWM_DRIVE_LEFT = 21	# ENA - H-Bridge enable pin
FORWARD_LEFT_PIN = 26	# IN1 - Forward Drive
REVERSE_LEFT_PIN = 19	# IN2 - Reverse Drive
# Motor B, Right Side GPIO CONSTANTS
PWM_DRIVE_RIGHT = 5		# ENB - H-Bridge enable pin
FORWARD_RIGHT_PIN = 13	# IN1 - Forward Drive
REVERSE_RIGHT_PIN = 6	# IN2 - Reverse Drive
 
# Initialise objects for H-Bridge GPIO PWM pins
# Set initial duty cycle to 0 and frequency to 1000
driveLeft = PWMOutputDevice(PWM_DRIVE_LEFT, True, 0, 1000)
driveRight = PWMOutputDevice(PWM_DRIVE_RIGHT, True, 0, 1000)
 
# Initialise objects for H-Bridge digital GPIO pins
forwardLeft = PWMOutputDevice(FORWARD_LEFT_PIN)
reverseLeft = PWMOutputDevice(REVERSE_LEFT_PIN)
forwardRight = PWMOutputDevice(FORWARD_RIGHT_PIN)
reverseRight = PWMOutputDevice(REVERSE_RIGHT_PIN)
 
def allStop():
	forwardLeft.value = False
	reverseLeft.value = False
	forwardRight.value = False
	reverseRight.value = False
	driveLeft.value = 0
	driveRight.value = 0
 
def spinRight():
	forwardLeft.value = True
	reverseLeft.value = False
	forwardRight.value = True
	reverseRight.value = False
	driveLeft.value = 1.0
	driveRight.value = 1.0
 
def spinLeft():
	forwardLeft.value = False
	reverseLeft.value = True
	forwardRight.value = False
	reverseRight.value = True
	driveLeft.value = 1.0
	driveRight.value = 1.0
 
def reverseDrive():
	forwardLeft.value = False
	reverseLeft.value = True
	forwardRight.value = True
	reverseRight.value = False
	driveLeft.value = 1.0
	driveRight.value = 1.0
 
def forwardDrive():
	forwardLeft.value = True
	reverseLeft.value = False
	forwardRight.value = False
	reverseRight.value = True
	driveLeft.value = 1.0
	driveRight.value = 1.0
 
def reverseTurnLeft():
	forwardLeft.value = True
	reverseLeft.value = False
	forwardRight.value = True
	reverseRight.value = False
	driveLeft.value = 1.0
	driveRight.value = 1.0
 
def forwardTurnRight():
	forwardLeft.value = True
	reverseLeft.value = False
	forwardRight.value = True
	reverseRight.value = False
	driveLeft.value = 1.0
	driveRight.value = 1.0
 
def forwardTurnLeft():
	forwardLeft.value = False
	reverseLeft.value = True
	forwardRight.value = False
	reverseRight.value = True
	driveLeft.value = 1.0
	driveRight.value = 1.0
 
def reverseTurnRight():
	forwardLeft.value = False
	reverseLeft.value = True
	forwardRight.value = False
	reverseRight.value = True
	driveLeft.value = 1.0
	driveRight.value = 1.0

def ping(): 
        p.ChangeDutyCycle(12.5) #180 - Left
        sleep(1)
        pul()
        if(distance>75.00):
            p.ChangeDutyCycle(7.5)
            spinLeft()
            sleep(2)
            allStop()
            sleep(2)
            drive()
        p.ChangeDutyCycle(10) #135 - Front-left
        sleep(1)
        pul()
        if(distance>75.00):
            p.ChangeDutyCycle(7.5)
            spinLeft()
            sleep(1)
            allStop()
            sleep(2)
            drive()
        #p.ChangeDutyCycle(7.5) #90 - Front
        #sleep(1)
        #pul()
        p.ChangeDutyCycle(5) #45 - Front-right
        sleep(1)
        pul()
        if(distance>75.00):
            p.ChangeDutyCycle(7.5)
            spinRight()
            sleep(1)
            allStop()
            sleep(2)
            drive()
        p.ChangeDutyCycle(2.5) #0 - Right
        sleep(1)
        pul()
        if(distance>75.00):
            p.ChangeDutyCycle(7.5)
            spinRight()
            sleep(2)
            allStop()
            sleep(2)
            drive()
        p.ChangeDutyCycle(7.5)
        reverseDrive()
        sleep(2)
        allStop()
        sleep(2)
        spinRight()
        sleep(3)
        allStop()
        sleep(2)
        drive()
        
def pul():
        global pulse_start
        global pulse_end
        global distance
        GPIO.output(TRIG, False)
        time.sleep(1) 
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
   
        while GPIO.input(ECHO)==0:
            pulse_start = time.time() 
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
    
        pulse_duration = pulse_end - pulse_start 
        distance = pulse_duration * 17150 
        distance = round(distance, 2)
        print ("Distance:",distance,"cm" )
        
def rev_alarm():
        a=GPIO.input(22)
        if(a==1):
                GPIO.output(17,True)
        else:
                GPIO.output(17,False)

def drive():
	forwardDrive()
	while True:
		pul()
		if(distance<75.00):
			allStop()
			ping()
			rev_alarm()

while True:
    drive()