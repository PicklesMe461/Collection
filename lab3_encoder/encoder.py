import machine
from machine import Pin, ADC
import time

# Create ADC objects for the QRD sensors
qrdA = ADC(Pin(26))
qrdB = ADC(Pin(27))

# Define threshold values for the QRD sensors
threshold = 40000

# Delay for reading
delay = 0.25

# Create states for the QRD sensors
qrdAState = [0]
qrdBState = [0]

# Create a list for pulses
pulses = []

# Forward marker for direction
forward = ""

def getQRDState(qrd, threshold):
    if qrd.read_u16() > threshold:
        return 1 # 1 is black
    else:
        return 0 # 0 is white
    
def pulse():
    print("Pulse")
    print("Forward: " + forward)
    pulses.append(time.ticks_ms())

    

def x1():
    # Change happens when one of the QRD sensors detects black, while the other one is on white
    global forward
    global qrdAState
    global qrdBState
    global threshold
    global delay
    counter = 0
    
    while True:
        qrdAState.append(getQRDState(qrdA, threshold))
        qrdBState.append(getQRDState(qrdB, threshold))
        if qrdAState[1] == 1 and qrdAState[0] == 0 and qrdBState[1] == 0:
            forward = "A"
            pulse()
            counter = counter +1
            print("Counter: ", counter)
        elif qrdBState[1] == 1 and qrdBState[0] == 0 and qrdAState[1] == 0:
            forward = "B"
            pulse()
            counter = counter + 1
            print("Counter: ", counter)
        
        
        if len(qrdAState) >= 2:
            qrdAState.pop(0)
            qrdBState.pop(0)

def x2():
    # Pulse happens when the forward sensor changes
    #the old value of the forward sensor is equal to the new value of the back sensor
    global forward
    global qrdAState
    global qrdBState
    global threshold
    global delay
    counter = 0

    while True:
        qrdAState.append(getQRDState(qrdA, threshold))
        qrdBState.append(getQRDState(qrdB, threshold))
        if qrdAState[0] == qrdBState[1] and qrdBState[1] != qrdBState[0]:
            forward = "A"
            pulse()
            counter = counter + 1
            print("Counter: ", counter)
        elif qrdBState[0] == qrdAState[1] and qrdAState[1] != qrdAState[0]:
            forward = "B"
            pulse()
            counter = counter + 1
            print("Counter: ", counter)
        time.sleep(delay)
        
        if len(qrdAState) >= 2:
            qrdAState.pop(0)
            qrdBState.pop(0)


def x4():
    global forward
    global qrdAState
    global qrdBState
    global threshold
    global delay
    counter = 0
    # Pulse happens when any value changes
    while True:
        qrdAState.append(getQRDState(qrdA, threshold))
        qrdBState.append(getQRDState(qrdB, threshold))
        if qrdAState[0] != qrdAState[1] or qrdBState[0] != qrdBState[1]:
            pulse()
            counter = counter + 1
            print("Counter: ", counter)
        time.sleep(delay)
        
        
        if len(qrdAState) >= 2:
            qrdAState.pop(0)
            qrdBState.pop(0)

def qrdTest():
    while True:
        print("QRD A reads: \n")
        print(getQRDState(qrdA, threshold))
        print("QRD B reads: \n")
        print(getQRDState(qrdB, threshold))
        time.sleep(delay)


x4()