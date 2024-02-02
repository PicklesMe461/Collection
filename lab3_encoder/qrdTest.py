import machine
from machine import Pin, ADC
import time


qrdA = ADC(Pin(26))
qrdB = ADC(Pin(27))

while True:
    print("QRD A reads: \n")
    print(qrdA.read_u16())
    print("QRD B reads: \n")
    print(qrdB.read_u16())
    time.sleep(0.5)