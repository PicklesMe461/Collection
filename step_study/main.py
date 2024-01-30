# Pico stepper Shooter 
# Hardware setup:
#    Stepper motor via DRV8833 driver breakout on GP21, GP20, GP19, GP18
#    External power supply

# Import required modules
import time
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import stepper


# Led setup test
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

# Blink for test
def blink(times):
    for _ in range(times):
        led.value = False
        time.sleep(0.1)
        led.value = True
        time.sleep(0.1)

# Stepper setup
DELAY = 0.006  # fastest is ~ 0.004, 0.01 is still very smooth, gets steppy after that
STEPS = 513  # this is a full 360º
coils = (
    DigitalInOut(board.GP21),  # A1
    DigitalInOut(board.GP20),  # A2
    DigitalInOut(board.GP19),  # B1
    DigitalInOut(board.GP18),  # B2
)
for coil in coils:
    coil.direction = Direction.OUTPUT

stepper_motor = stepper.StepperMotor(
    coils[0], coils[1], coils[2], coils[3], microsteps=None
)


def stepper_fwd():
    print("stepper forward")
    for _ in range(STEPS):
        stepper_motor.onestep(direction=stepper.FORWARD)
        time.sleep(DELAY)
    stepper_motor.release()


def stepper_back():
    print("stepper backward")
    for _ in range(STEPS):
        stepper_motor.onestep(direction=stepper.BACKWARD)
        time.sleep(DELAY)
    stepper_motor.release()


def run_test(testnum):
    if testnum is 0:
        stepper_fwd()
    elif testnum is 1:
        stepper_back()


while True:
    run_test(0)
    blink(3)
    run_test(1)