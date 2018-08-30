#! /usr/bin/env python3.6

import time
import RPi.GPIO as GPIO

class motorControl:
    # motor1 and motor2 are lists containing the two pins numbers necessary to control the motor
    def __init__(self, motor1, motor2):
        self._CONSTANT1 = 5
        self._CONSTANT2 = 10
        
        self.motor = motor1+motor2

        # use Broadcom SOC channel numbers
        GPIO.setmode(GPIO.BCM)
        
        # set all pins to output and low
        for pin in self.motor:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
       
        # create list of PWM objects with frequency of 490Hz
        self.pwm = [GPIO.PWM(pin, 490) for pin in self.motor]
        
        # initialize all with 0% duty cycle
        for pwm in self.pwm:
            pwm.start(0)
             
    def __enter__(self):
        return self

    def __exit__(self, *args):
        for pwm in self.pwm:
            pwm.stop()
        GPIO.cleanup()
    
    # vel is a velocity vector
    def cmd_vel(self, vel):
        x_vel = vel[0]
        y_vel = vel[1]
        
        pinIndex1 = 0
        pinIndex2 = 2
        
        if y_vel < 0:
            pinIndex1 = 1
            pinIndex2 = 3
            
        if x_vel > 0:
            vel1 = self._CONSTANT1 * x_vel
            vel2 = self._CONSTANT2 * x_vel
        elif x_vel < 0:
            vel1 = self._CONSTANT2 * x_vel
            vel2 = self._CONSTANT1 * x_vel 
        else:
            vel1 = 
            if y_vel == 0:
                vel1 = 0
            vel2 = vel1
            
        self.pwm[pinIndex1].ChangeDutyCycle(vel1)
        self.pwm[pinIndex2].ChangeDutyCycle(vel2)
        self.pwm[abs(pinIndex1-1)].ChangeDutyCycle(0)
        self.pwm[abs(pinIndex1-3)+2].ChangeDutyCycle(0)
