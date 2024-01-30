
import board

from digitalio import DigitalInOut, Direction
from adafruit_motor import motor as Motor
from pwmio import PWMOut







# Motors set up
#Green Wire
default_frequency = 100
motor4a = PWMOut(board.GP21, frequency=default_frequency)
#Yellow Wire
motor3a = PWMOut(board.GP20, frequency=default_frequency)
motor_throttle = 1
motorLed = Motor.DCMotor(motor3a, motor4a)


while True:
    motorLed.throttle = motor_throttle
    print(f"Motor throttle is set to {motorLed.throttle}.")