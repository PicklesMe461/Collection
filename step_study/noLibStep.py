import board
import time
import digitalio

wire1 = digitalio.DigitalInOut(board.GP18)
wire1.direction = digitalio.Direction.OUTPUT

wire2 = digitalio.DigitalInOut(board.GP19)
wire2.direction = digitalio.Direction.OUTPUT


wire3 = digitalio.DigitalInOut(board.GP20)
wire3.direction = digitalio.Direction.OUTPUT

wire4 = digitalio.DigitalInOut(board.GP21)
wire4.direction = digitalio.Direction.OUTPUT

wires = [wire1, wire2, wire3, wire4]

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


continious_rotation("CW")
