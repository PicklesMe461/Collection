import machine
from machine import Pin, ADC
import time

# Create ADC objects for the QRD sensors
qrdA = ADC(Pin(26))
qrdB = ADC(Pin(27))

def print_values():
    while True:
        print("QRD A: {}, QRD B : {}".format(qrdA.read_u16(), qrdB.read_u16()))
        time.sleep(0.5)

def calculate_distance():
    dist = 4 #cm
    while True:
        _range = abs((int(qrdA.read_u16())-int(qrdB.read_u16()))/int(qrdA.read_u16()))*100
        curr_dist = 4*_range
        print(curr_dist)
        time.sleep(0.5)
    return curr_dist    

calculate_distance()