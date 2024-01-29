import board
import digitalio
import time
import analogio
import microcontroller
import pwmio
import time

#Red Button Right Pulled up
btn_red = digitalio.DigitalInOut(board.GP22)
btn_red.direction = digitalio.Direction.INPUT
btn_red.pull = digitalio.Pull.UP

#Blue Button Left Pulled down
btn_blue = digitalio.DigitalInOut(board.GP14)
btn_blue.direction = digitalio.Direction.INPUT
btn_blue.pull = digitalio.Pull.DOWN

#Potentiometer
pot = analogio.AnalogIn(board.GP26)

default_cycle = 32768 # 50% duty cycle used because I couldn't see the difference between 100% and 50% duty cycle
debounce_interval = 0.01 # 10ms debounce interval

pwm_led1 = pwmio.PWMOut(board.GP2, frequency=5000, duty_cycle=0)
pwm_led2 = pwmio.PWMOut(board.GP3, frequency=5000, duty_cycle=0)
pwm_led3 = pwmio.PWMOut(board.GP4, frequency=5000, duty_cycle=0)
pwm_led4 = pwmio.PWMOut(board.GP5, frequency=5000, duty_cycle=0)
pwm_led5 = pwmio.PWMOut(board.GP6, frequency=5000, duty_cycle=0)
pwm_led6 = pwmio.PWMOut(board.GP7, frequency=5000, duty_cycle=0)
pwm_led7 = pwmio.PWMOut(board.GP8, frequency=5000, duty_cycle=0)
pwm_led8 = pwmio.PWMOut(board.GP9, frequency=5000, duty_cycle=0)
pwm_leds = [pwm_led1, pwm_led2, pwm_led3, pwm_led4, pwm_led5, pwm_led6, pwm_led7, pwm_led8]

ledboard = digitalio.DigitalInOut(board.LED)
ledboard.direction = digitalio.Direction.OUTPUT

def read_pot():
    return pot.value

#Function to take an input value, convert it to bytes and display it across 8 leds
def ByteDisplay(val=0):
    val = int(val)
    if val > 255:
        val = 255
    elif val < 0:
        val = 0
    binary_val = bin(val)[2:]
    while len(binary_val) < 8:
        binary_val = '0' + binary_val
    for i, pwm_led in enumerate(pwm_leds):
        pwm_led.duty_cycle = int(binary_val[i]) * default_cycle
    print("ByteDisplayed " + str(val))
    return True

# Can also use left and right bit shift ops
# Or masking and bit checking

# bin(8/2) diyince shift ediyor
# Mesela bin4 0b100 normalde bin8 0b1000
# yani bolunce sola shift ediyor

def LightAll():
    for pwm_led in pwm_leds:
        pwm_led.duty_cycle = default_cycle
    print("LightAll")
    return True

def LightNone():
    for pwm_led in pwm_leds:
        pwm_led.duty_cycle = 0
    print("LightNone")
    return True

#Function to light up each LED with a custom speed one at a time
def Volta(N=3, speed=0.1):
    
    for i in range(N):
        for pwm_led in pwm_leds:
            pwm_led.duty_cycle = default_cycle
            time.sleep(0.01 / speed)
            pwm_led.duty_cycle = 0
        for pwm_led in reversed(pwm_leds):
            
            pwm_led.duty_cycle = default_cycle
            time.sleep(0.01 / speed)
            pwm_led.duty_cycle = 0
        print("Volta")
    return True


# Deprecated
def SnakeNot(L=3, speed=0.1):
    for i in range(L):
        for pwm_led in pwm_leds:
            pwm_led.duty_cycle = default_cycle
            time.sleep(0.01 / speed)
            pwm_led.duty_cycle = 0
        for pwm_led in reversed(pwm_leds):
            pwm_led.duty_cycle = default_cycle
            time.sleep(0.01 / speed)
            pwm_led.duty_cycle = 0
        print("Snake")
    return True

# Cuysal Fade
def fade(pwm_leds):
  for led in pwm_leds:
    for i in range(100):
      if i < 50:
        led.duty_cycle = int(i * 2 * default_cycle / 100)  # Up
      else:
        led.duty_cycle = default_cycle - int((i - 50) * 2 * default_cycle / 100)  # Down 
      time.sleep(0.0125/4)



def SnakeC(L = 3, speed = 0.1):
    increase = 1
    i = 2
    while True:
        if increase > 0:
            if i >= 3:
                pwm_leds[i-3].duty_cycle = 0
                pwm_leds[i-2].duty_cycle = 0
            fade(pwm_leds[i-2:i+1])

            if i == 7:
                increase *= -1

        else:
            if i <= 6:
                pwm_leds[i+1].duty_cycle = 0
            print(i-2,i-1,i)
            fade(pwm_leds[i:i-3:-1])

            if i == 2:
                increase *= -1
            
        i += increase



# Function to fade in
def FadeIn(led):
    for i in range(100):
        led.duty_cycle = int(i * 2 * default_cycle / 100)  # Up
        time.sleep(0.0125/4)
    return True

# Function to fade out
def FadeOut(led):
    for i in range(100):
        led.duty_cycle = default_cycle - int((i - 50) * 2 * default_cycle / 100)  # Down 
        time.sleep(0.0125/4)
    return True

def Snake(L = 3, speed = 0.1):
    pos = 0
    duty_cycles = []
    # For loop to determine L duty cycle values up to default_cycle
    for i in range(L):
        duty_cycles.append(int(default_cycle / L * (i + 1)))

    while True:
        # For loop to light up the LEDs from 0 to L

        for i in range(L):
            if pos + i >= 8:
                for j in range(L):
                    pwm_leds[pos + i -j - 1].duty_cycle = 0
                    time.sleep(0.01 / speed)
                # Now in reverse
                pos = 8
                while pos > L-1:
                    for j in range(L):
                        pwm_leds[pos - j - 1].duty_cycle = duty_cycles[j]
                        time.sleep(0.01 / speed)
                    pos -= 1
                    pwm_leds[pos].duty_cycle = 0
                
                for j in range(L):
                    pwm_leds[pos - j - 1].duty_cycle = 0
                    time.sleep(0.01 / speed)

                pos = 0
                i = 0
 
            pwm_leds[i + pos].duty_cycle = duty_cycles[i]
            time.sleep(0.01 / speed)
        pwm_leds[pos].duty_cycle = 0
        pos += 1
        print("Snake")


    return True



def Breathe(breathe_mode = 0):
    if breathe_mode == 0:
        while True:
            for i in range(100):
                # PWM LED up and down
                if i < 50:
                    for pwm_led in pwm_leds:
                        pwm_led.duty_cycle = int(i * 2 * default_cycle / 100) #Up
                else:
                    for pwm_led in pwm_leds:
                        pwm_led.duty_cycle = int((100 - i) * 2 * default_cycle / 100) #Down
                time.sleep(0.01)

    if breathe_mode == 1:
        while True:
            for i in range(0, default_cycle, 256):
                for pwm_led in pwm_leds:
                    pwm_led.duty_cycle = i
                time.sleep(0.01)
            for i in range(default_cycle, 0, -256):
                for pwm_led in pwm_leds:
                    pwm_led.duty_cycle = i
                time.sleep(0.01)
    while True:
        for i in range(0, 50000, 256):
            for pwm_led in pwm_leds:
                pwm_led.duty_cycle = i
            time.sleep(0.01)
        for i in range(5000, 0, -256):
            for pwm_led in pwm_leds:
                pwm_led.duty_cycle = i
            time.sleep(0.01)
    return True

#Function to light up each LED one at a time
def LightOne():
    for pwm_led in pwm_leds:
        pwm_led.duty_cycle = default_cycle
        time.sleep(0.5)
        pwm_led.duty_cycle = 0
    print("LightOne")
    return True

#Function to light up the LEDs in laoding pattern
def LightLoading():
    for pwm_led in pwm_leds:
        pwm_led.duty_cycle = 0
    time.sleep(0.5)
    for pwm_led in pwm_leds:
        pwm_led.duty_cycle = default_cycle
        time.sleep(0.5)
        pwm_led.duty_cycle = 0
    time.sleep(0.5)
    print("LightLoading")
    return True

# A function to light up the LEDs according to the potentiometer byte value
def LightPotByte():
    while True:
        pot_value = read_pot()
        pot_value = int(pot_value / 65535 * 256)
        ByteDisplay(pot_value)
        print(pot_value)
        time.sleep(0.2)
    return True

# A function to light up the LEDs according to the potentiometer percent
def LightPot():
    while True:
        pot_value = read_pot()
        pot_value = int(pot_value / 65535 * 100)
        for i, pwm_led in enumerate(pwm_leds):
            if i < pot_value / 100 * 8:
                pwm_led.duty_cycle = default_cycle
            else:
                pwm_led.duty_cycle = 0
        print(pot_value)
        time.sleep(0.2)
    return True

#Function to wait for pin change
def WaitForPinChange(pin):
    pin_state = pin.value
    active = 0
    while active < 20:
        if pin.value != pin_state:
            active += 1
        else:
            active = 0
        


#Function to print button value
def Button():
    if btn_red.value == False:
        print("Red Button Pressed")
    elif btn_blue.value == True:
        print("Blue Button Pressed")
    else:
        print("No Button Pressed")
    return True

#A button controlled counter function to count up to 255 and display it on the LEDs
def Button_Count():
    val = generate_random_number()
    ByteDisplay(val)
    pressed = False
    print(val)
    while True:
        while not pressed:
            if btn_red.value == False and pressed == False:
                pressed = True
                val += 1
                ByteDisplay(val)
                print(val)
                time.sleep(debounce_interval)
                WaitForPinChange(btn_red)
            elif btn_blue.value == True and pressed == False:
                pressed = True
                val -= 1
                ByteDisplay(val)
                print(val)
                time.sleep(debounce_interval)
                WaitForPinChange(btn_blue)
        if btn_red.value == True and pressed == True:
            pressed = False
            time.sleep(debounce_interval)
        elif btn_blue.value == False and pressed == True:
            pressed = False
            time.sleep(debounce_interval)
        else:
            ByteDisplay(val)
            print(val)
            time.sleep(debounce_interval)



def generate_random_number():
    # Get the current time in milliseconds
    current_time = int(time.time() * 1000)
    
    # Use the current time and cpu temp as the seed for the random number generator
    seed = current_time * round(microcontroller.cpu.temperature) % 256
    
    # Generate a random number using the seed
    random_number = (seed * 1103515245 + 12345) % 256
    
    
    return random_number


#Function to display the onboard temperature value on the LEDs
def Temp():
    temp = 0
    while True:
        temp = round(microcontroller.cpu.temperature)
        ByteDisplay(temp)
        print(temp)
        time.sleep(0.2)
    return True

def Menu():
    mode_val = input("Enter a mode between 2 to 7: ")
    if mode_val == "2":
        print("You chose ByteDisplay")
        byteValue = int(input("Enter a value between 0 to 255: "))
        if byteValue > 255:
            byteValue = 255
            print("Value too high, setting to 255")
        while True:
            ByteDisplay(byteValue)
    elif mode_val == "3":
        print("You chose Walking Lights")
        Volta()
    elif mode_val == "4":
        print("You chose walking and fading lights")
        
        Snake()
        
    elif mode_val == "5":
        print("You chose Button Counter")
        Button_Count()
    elif mode_val == "6":
        print("You chose digital VU meter")
        LightPot()
    elif mode_val == "7":
        print("You chose Temperature Display")
        Temp()
    else:
        print("Invalid Mode")