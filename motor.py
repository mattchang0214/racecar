#! /usr/bin/env python3.6

import time
import RPi.GPIO as GPIO

# define constants
MOTOR1 = 13 # bottom motor pin
MOTOR2 = 19 # top motor pin
MOTOR3 = 20 # top motor pin
MOTOR4 = 16 # bottom motor pin

# define in/out pins
def setup(*pins):
    # use Broadcom SOC channel numbers
    GPIO.setmode(GPIO.BCM)
    
    # set all pins to output and low
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

# f for forward, r for reverse, s for stop
def runMotor(pin1, pin2, direction="s"):
    if direction == "f":
        GPIO.output(pin1, GPIO.HIGH)
        GPIO.output(pin2, GPIO.LOW)
        print("Forward")
    elif direction == "r":
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.HIGH)
        print("Reverse")
    else:
        GPIO.output(pin1, GPIO.LOW)
        GPIO.output(pin2, GPIO.LOW)

if __name__ == "__main__":
    setup(MOTOR1, MOTOR2, MOTOR3, MOTOR4)
    print("Starting")
    
    try:
        while True:
            runMotor(MOTOR1, MOTOR2, "f")
            runMotor(MOTOR3, MOTOR4, "f")
            time.sleep(3)
            runMotor(MOTOR1, MOTOR2)
            runMotor(MOTOR3, MOTOR4)
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting")
        GPIO.cleanup()
