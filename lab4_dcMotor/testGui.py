import tkinter as tk
import requests


# Create a Tkinter window
window = tk.Tk()
window.title("LED Control")
window.geometry("400x200")

# Function to send a POST request to the server to turn the LED on
def turn_on():
    requests.post("http://192.168.68.110/", data={"LED" : "ON"})

# Function to send a POST request to the server to turn the LED off
def turn_off():
    requests.post("http://192.168.68.110/", data={"LED" : "OFF"})

# Create buttons to control the LED
on_button = tk.Button(window, text="Turn On", command=turn_on)
on_button.pack(pady=10)

off_button = tk.Button(window, text="Turn Off", command=turn_off)
off_button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()