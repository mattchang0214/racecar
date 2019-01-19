#! /usr/bin/env python3.6

import time
import RPi.GPIO as GPIO

class motorControl:
    # motor1 and motor2 are lists containing the two pins numbers necessary to control the motor
    def __init__(self, motor1, motor2):
        self._CONSTANT1 = 0.15
        self._CONSTANT2 = 0.08
        
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
        pinIndex2 = 3
        
        if y_vel > 0:
            pinIndex1 = 1
            pinIndex2 = 2
            
        if x_vel > 0:
            vel1 = self._CONSTANT1 * x_vel
            vel2 = self._CONSTANT2 * x_vel
        elif x_vel < 0:
            vel1 = abs(self._CONSTANT2 * x_vel)
            vel2 = abs(self._CONSTANT1 * x_vel)
        else:
            vel1 = abs(self._CONSTANT2 * y_vel)
            vel2 = vel1
        
        if vel1 < 22 and vel2 < 22:
            vel1 = 22
            vel2 = 22

        print("vel: ({0},{1})".format(vel1, vel2))
        self.pwm[pinIndex1].ChangeDutyCycle(vel1)
        self.pwm[pinIndex2].ChangeDutyCycle(vel2)
        self.pwm[abs(pinIndex1-1)].ChangeDutyCycle(0)
        self.pwm[abs(pinIndex2-3)+2].ChangeDutyCycle(0)

if __name__ == '__main__':
    with motorControl([13, 19], [20, 16]) as motCon:
        motCon.cmd_vel([0, 5])
        time.sleep(1)
        motCon.cmd_vel([4, 4])
        time.sleep(1)
        motCon.cmd_vel([-4, 4])
        time.sleep(2)
        motCon.cmd_vel([4, 4])
        time.sleep(1)
        motCon.cmd_vel([0, 0])
        time.sleep(1)
