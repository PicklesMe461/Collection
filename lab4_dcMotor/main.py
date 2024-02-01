# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# SWITCH BETWEEN MANUAL AND WEB CONTROL BY COMMENTING OUT THE OTHER


import os
import time
import ipaddress
import wifi
import socketpool
import busio
import board
from analogio import AnalogIn
import microcontroller
from digitalio import DigitalInOut, Direction
from adafruit_httpserver import Server, Request, Response, POST
import helpers
import digitalio
from adafruit_motor import motor as Motor
from pwmio import PWMOut

# Motors set up
#Green Wire
default_frequency = 100
motor4a = PWMOut(board.GP17, frequency=default_frequency, variable_frequency=True)
#Yellow Wire
motor3a = PWMOut(board.GP18, frequency=default_frequency, variable_frequency=True)
motor_throttle = 0.9
motorLed = Motor.DCMotor(motor3a, motor4a)
motorLed.throttle = motor_throttle

#white Button Right Pulled up
btn_white = digitalio.DigitalInOut(board.GP22)
btn_white.direction = digitalio.Direction.INPUT
btn_white.pull = digitalio.Pull.UP

#Blue Button Left Pulled down
btn_blue = digitalio.DigitalInOut(board.GP14)
btn_blue.direction = digitalio.Direction.INPUT
btn_blue.pull = digitalio.Pull.DOWN

# Pot
pot = AnalogIn(board.GP26)

def printMotorStatus(motor):
    print(f"Motor throttle is set to {motor.throttle}.")

def manualRide():
        buttonR_pressed = False
        buttonL_pressed = False
        manual_throttle = pwm_converter(pot.value)
        manual_direction = 1
        while True:
            manual_throttle = pwm_converter(pot.value) * manual_direction
            if btn_white.value == False:
                buttonR_pressed = True
                buttonL_pressed = False
            elif btn_blue.value == True:
                buttonL_pressed = True
                buttonR_pressed = False

            if buttonR_pressed:
                print("CW")
                manual_direction = 1
            elif buttonL_pressed:
                print("CCW")
                manual_direction = -1

            motorLed.throttle = manual_throttle 
            
            print("Motor throttle is set to: ", manual_throttle)

            time.sleep(0.1)
    

# function to convert potentiometer value to pwm throttle
def pwm_converter(value):
    scaled_value = (value/65535)
    return scaled_value


# SWITCH BETWEEN MANUAL AND WEB CONTROL BY COMMENTING OUT THE OTHER
manualRide()

#  onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

#  connect to network
print()
print("Connecting to WiFi")
#  connect to your SSID
wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
print("Connected to WiFi")

pool = socketpool.SocketPool(wifi.radio)
print("pool created")
server = Server(pool, "/static", debug=True)
print("server created")

#  route default static IP
@server.route("/")
def base(request: Request):  # pylint: disable=unused-argument
    #  serve the HTML f string
    #  with content type text/html
    return Response(request, f"{webpage()}", content_type='text/html')


#  if a button is pressed on the site
@server.route("/", POST)
def buttonpress(request: Request):
    global motor_throttle
    global motorLed

    #  get the raw text
    raw_text = request.raw_request.decode("utf8")
    print(raw_text)
    #  if the led on button was pressed
    if "ON" in raw_text:
        #  turn on the onboard LED
        led.value = True
    #  if the led off button was pressed
    if "OFF" in raw_text:
        #  turn the onboard LED off
        led.value = False
    #  reload site
    if "CW" in raw_text:
        # Set Motor direction to clockwise
        print("CW")
        motor_throttle = abs(motorLed.throttle)
        motorLed.throttle = motor_throttle

    if "CCW" in raw_text:
        # Set Motor direction to counter-clockwise
        print("CCW")
        motor_throttle = abs(motorLed.throttle) * -1
        motorLed.throttle = motor_throttle

    if "START" in raw_text:
        # Start Motor
        print("START")
        motorLed.throttle = motor_throttle

    if "STOP" in raw_text:
        # Stop Motor
        print("STOP")
        motorLed.throttle = 0

    if "FREQUENCY" in raw_text:
        # Set Motor PWM frequency
        print("FREQUENCY")
        try:
            new_frequency = int(raw_text.split("FREQUENCY+")[1].split("=")[0])
        except Exception as e:
            new_frequency = int(raw_text.split("FREQUENCY=")[1])
        
        print(new_frequency)
        motor4a.frequency = new_frequency
        motor3a.frequency = new_frequency
        motorLed.throttle = motor_throttle

    if "RELEASE" in raw_text:
        # Release Motor
        print("RELEASE")
        motorLed.throttle = None
        
    if "PWM" in raw_text:
        # Set Motor PWM
        try:
            # Get the PWM value from raw text

            try:
                pwm = raw_text.split("PWM+")[1].split("=")[0]
            except Exception as e:
                pwm = raw_text.split("PWM=")[1]
            print(pwm)
            motor_throttle = int(pwm) / 100
            print("Motor throttle is set to: ", motor_throttle)
            # Set the motor throttle
            motorLed.throttle = motor_throttle * helpers.sign(motor_throttle)
            print(motorLed)
        except Exception as e:
            print("Exception ", e)
            print("PWM value not found")
            print(raw_text)

    
    return Response(request, f"{webpage()}", content_type='text/html')



#  variables for testing HTML
temp_test = helpers.Temp()
unit = "C"
#  font for HTML
font_family = "monospace"


#  the HTML script
#  setup as an f string
#  this way, can insert string variables from code.py directly
#  of note, use {{ and }} if something from html *actually* needs to be in brackets
#  i.e. CSS style formatting

def webpage():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-type" content="text/html;charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    html{{font-family: {font_family}; background-color: lightgrey;
    display:inline-block; margin: 0px auto; text-align: center;}}
      h1{{color: deeppink; width: 200; word-wrap: break-word; padding: 2vh; font-size: 35px;}}
      p{{font-size: 1.5rem; width: 200; word-wrap: break-word;}}
      .button{{font-family: {font_family};display: inline-block;
      background-color: black; border: none;
      border-radius: 4px; color: white; padding: 16px 40px;
      text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}}
      p.dotted {{margin: auto;
      width: 75%; font-size: 25px; text-align: center;}}
    </style>
    </head>
    <body>
    <title>Pico W HTTP Server</title>
    <h1>Pico W HTTP Server</h1>
    <br>
    <p class="dotted">This is a Pico W running an HTTP server with CircuitPython.</p>
    <br>
    <p class="dotted">The current ambient temperature near the Pico W is
    <span style="color: deeppink;">{temp_test:.2f}°{unit}</span></p><br>
    <h1>Control the LED on the Pico W with these buttons:</h1><br>
    <form accept-charset="utf-8" method="POST">
    <button class="button" name="LED ON" value="ON" type="submit">LED ON</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="LED OFF" value="OFF" type="submit">LED OFF</button></a></p></form>
    <h1>Motor?</h>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="CW" value="CW" type="submit">CW</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="CCW" value="CCW" type="submit">CCW</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="PWM 50" value="PWM 50" type="submit">PWM 50</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="PWM 90" value="PWM 90" type="submit">PWM 90</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="CCW" value="STOP" type="submit">STOP</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="FREQUENCY 1000" value="FREQUENCY 1000" type="submit">FREQUENCY 1000</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="FREQUENCY 60" value="FREQUENCY 60" type="submit">FREQUENCY 60</button></a></p></form>
    </body></html>
    """
    return html



# SWITCH BETWEEN MANUAL AND WEB CONTROL BY COMMENTING OUT THE OTHER
#server.serve_forever(str(wifi.radio.ipv4_address))
