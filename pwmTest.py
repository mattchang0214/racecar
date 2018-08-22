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
    GPIO.setmode(GPIO.BCM)
    
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

if __name__ == "__main__":
    setup(MOTOR1, MOTOR2, MOTOR3, MOTOR4)
    
    # create PWM objects
    pwm1 = GPIO.PWM(MOTOR1, 100)
    pwm2 = GPIO.PWM(MOTOR3, 100)
    
    # initialize with 50% duty cycle (~1.6 V)
    pwm1.start(50)
    pwm2.start(50)
    
    time.sleep(2)
    try:
        while True:
            pwm1.ChangeDutyCycle(100)
            pwm2.ChangeDutyCycle(100)
            time.sleep(2)
            pwm1.ChangeDutyCycle(50)
            pwm2.ChangeDutyCycle(80)
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting")
        pwm1.stop()
        pwm2.stop()
        GPIO.cleanup()
