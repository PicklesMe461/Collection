import time
import microcontroller




#Function to get the onboard temperature value on the LEDs
def Temp():
    temp = 0
    temp = round(microcontroller.cpu.temperature)
    return temp


#Function to decode
def decode(data):
    print("decoding")
    datastr = ''.join([chr(b) for b in data])  # convert bytearray to string
    return datastr

#Function to return the sign of an integer
def sign(x):
    if x >= 0:
        return 1
    else:
        return -1