import time
import wifi
import os
import socketpool
import bugeval
import picoeval
import decode
import microcontroller

data_buffer = bytearray(1024)
print("data buffer type: " + str(type(data_buffer)))
# function to connect to wifi and start ap server
def connect_start():
    # Connect to WiFi
    print("Connecting to wifi")
    try:
        wifi.radio.connect(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
        print("Connected to wifi")
    except Exception as e:
        print("Failed to connect to wifi")
        print("Error: " + str(e))
        return False
    return True


# function to start soft ap server
def start_soft_ap():
    ap_ssid = os.getenv("AP_SSID")
    ap_password = os.getenv("AP_PASSWORD")

    try:
        # Start an access point
        wifi.radio.enabled = True
        wifi.radio.start_ap(ssid = ap_ssid, password = ap_password)

        print("Soft Access Point started, not connected to the internet")
        print("SSID: " + ap_ssid)
        print("Password: " + ap_password)
        print("IP address: " + str(wifi.radio.ipv4_address_ap))
        pool = socketpool.SocketPool(wifi.radio)
        #Create a bugeval server
        server_socket = pool.socket()
        server_socket.bind((str(wifi.radio.ipv4_address_ap), 8882))
        server_socket.listen(1)
        print("Server is listening on " + str(wifi.radio.ipv4_address_ap) + ":8882")

        while True:
            client_socket, client_addr = server_socket.accept()
            print("Client connected from", client_addr)
            print("Waiting for data")
            while True:
                
                data = decode.decode(client_socket.recv_into(data_buffer))
                print("data: " + str(data))
                if not data:
                    break
                message_received = data
                print("Received message: " + message_received)
                # Evaluate the message
                result = picoeval.bugeval(message_received)
                print("Result: " + str(result))
                # Send the result back to the client
                client_socket.sendall(str(result).encode())
            client_socket.close()

    except Exception as e:
        print("Failed to start Access Point")
        print("Error: " + str(e))
        print("SSID: " + ap_ssid)
        print("Password: " + ap_password)
        print("IP address: " + str(wifi.radio.ipv4_address_ap))
        pool = socketpool.SocketPool(wifi.radio)
        #Create a bugeval server
        server_socket = pool.socket()
        server_socket.bind((str(wifi.radio.ipv4_address_ap), 8882))
        server_socket.listen(1)

        print("Server is listening on " + str(wifi.radio.ipv4_address_ap) + ":8882")

        while True:
            client_socket, client_addr = server_socket.accept()
            print("Client connected from", client_addr)
            while True:
                print("Waiting for data")
                client_socket.recv_into(data_buffer)
                message_received = decode.decode(data_buffer)
                print("Received message: " + message_received)
                if not message_received:
                    break
                # Evaluate the message
                result = picoeval.bugeval(message_received)
                print("Result: " + str(result))
                # Send the result back to the client
                client_socket.sendall(str(result).encode())
            client_socket.close()
        return False
    
