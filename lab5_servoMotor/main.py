# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials Servo standard servo example"""

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
pot = AnalogIn(board.GP27)

# Create a servo object, my_servo.
my_servo = servo.Servo(pwm_servo)

# HTTP Server setup
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
    global pwm_servo
    global my_servo

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


    if "RELEASE" in raw_text:
        # Release Motor
        print("RELEASE")
        my_servo.angle = None
        
    if "PWM" in raw_text:
        # Set Motor angle
        try:
            # Get the PWM value from raw text

            try:
                pwm = raw_text.split("PWM+")[1].split("=")[0]
            except Exception as e:
                pwm = raw_text.split("PWM=")[1]
            print(pwm)
            # Set the SERVO angle
            my_servo.angle = int(pwm)

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
    <button class="button" name="ANGLE 50" value="PWM 50" type="submit">ANGLE 50</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="ANGLE 90" value="PWM 90" type="submit">ANGLE 90</button></a></p></form>
    <p><form accept-charset="utf-8" method="POST">
    <button class="button" name="RELEASE" value="RELEASE" type="submit">RELEASE</button></a></p></form>
    </body></html>
    """
    return html





def angle_converter(value):
    scaled_value = (value/65535)*180
    return scaled_value

def RCServo_pos_Pot(flag):
    while flag:
        my_servo.angle = angle_converter(pot.value)
        time.sleep(0.1)

def RCServo_pos_REPL():
    while True:
        try:
            pos = float(input("Please enter the position(in angles[0-180]):"))

            my_servo.angle = pos

        except:
            print("Invalid value, please enter a floating number btw [0-180] range.")
            print("exiting...")
            break


def main():
    options = {"option 1" : "REPL", "option 2": "potentiometer"}
    print("----Servo Angle Control----")
    print("Option 1 - REPL\nOption 2 - Potentiometer")
    print("########---------########")
    option_input = input("Please make a mode selection:")

    if option_input == "REPL":
        RCServo_pos_REPL()
    elif option_input == "pot":
        RCServo_pos_Pot(True)

#main()

server.serve_forever(str(wifi.radio.ipv4_address))