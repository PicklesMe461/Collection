import board
import time
import digitalio
import helpers
import wifi
import socketpool
import os
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction
from adafruit_httpserver import Server, Request, Response, POST

wire1 = digitalio.DigitalInOut(board.GP10)
wire1.direction = digitalio.Direction.OUTPUT

wire2 = digitalio.DigitalInOut(board.GP11)
wire2.direction = digitalio.Direction.OUTPUT


wire3 = digitalio.DigitalInOut(board.GP12)
wire3.direction = digitalio.Direction.OUTPUT

wire4 = digitalio.DigitalInOut(board.GP13)
wire4.direction = digitalio.Direction.OUTPUT

wires = [wire1, wire2, wire3, wire4]

#  onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False



def wanted_rotation(wire_states, mode, delay=20):
    print(wire_states)
    coilNum = 0
    if mode == "continious":
        while True:
            coilNum = 0
            for state in wire_states:
                wires[coilNum].value = bool(state)
                coilNum += 1
            time.sleep(delay/1000)

    elif mode == "single":
        for state in wire_states:
            print(coilNum, wires[coilNum], wires[coilNum].value)
            wires[coilNum].value = bool(state)
            print(coilNum, wires[coilNum], wires[coilNum].value)
            coilNum += 1

        time.sleep(2)
        print(wire_states)
        print("--------------")
        print([wire.value for wire in wires])

    elif mode == "STOP":
        for state in wire_states:
            wires[coilNum].value = False
            coilNum += 1


def continious_rotation(key="CW"):
    if key == "CW":
        index = 3
        while True:
            if index == -1:
                index = 3

            wires[index].value = True
            wires[index-1].value = False
            time.sleep(0.01)
            wires[index].value = False
            time.sleep(0.01)

            index -= 1
    elif key== "CCW":
        index = 0
        while True:
            if index == 3:
                index = 0

            wires[index].value = True
            wires[index+1].value = False
            time.sleep(0.01)
            wires[index].value = False
            time.sleep(0.01)

            index += 1





#  connect to network
try:
    print()
    print("Connecting to WiFi")
    #  connect to your SSID
    wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
    print("Connected to WiFi")

    pool = socketpool.SocketPool(wifi.radio)
    print("pool created")
    server = Server(pool, "/static", debug=True)
    print("server created")
except Exception as e:
    print(e)
    print("No wifi connection")
    print("Exiting ... ")
    

#  route default static IP
@server.route("/")
def base(request: Request):  # pylint: disable=unused-argument
    #  serve the HTML f string
    #  with content type text/html
    return Response(request, f"{webpage()}", content_type='text/html')



#  if a button is pressed on the site
@server.route("/", POST)
def buttonpress(request: Request):

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


    if "STOP" in raw_text:
        # STOP Motor
        print("STOP")
        
        
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




