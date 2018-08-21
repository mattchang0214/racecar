#! /usr/bin/env python3.6

import time
import RPi.GPIO as GPIO

MOTOR1 = 12
MOTOR2 = 13


def setup(*pins):
    GPIO.setmode(GPIO.BCM)
    
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

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
    setup(MOTOR1, MOTOR2)
    print("Starting")
    
    try:
        while True:
            runMotor(MOTOR1, MOTOR2, "f")
            time.sleep(3)
            runMotor(MOTOR1, MOTOR2)
            time.sleep(1)
            runMotor(MOTOR1, MOTOR2, "r")
            time.sleep(3)
            runMotor(MOTOR1, MOTOR2)
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting")
        GPIO.cleanup()
