import time
import board
import pwmio
import wifi
import socketpool
import os
from adafruit_motor import servo
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction
from adafruit_httpserver import Server, Request, Response, POST
import helpers

# create a PWMOut object on Pin A2.
pwm_servo = pwmio.PWMOut(board.GP0, duty_cycle=2 ** 15, frequency=100)

# potentiometer setup.
pot = AnalogIn(board.GP26)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm_servo)

def angle_converter(value):
    scaled_value = (value/65535)*180
    return scaled_value


def RCServo_pos_Pot():
    
    my_servo.angle = angle_converter(pot.value)
    print(my_servo.angle)
    time.sleep(0.035)



RCServo_pos_Pot()