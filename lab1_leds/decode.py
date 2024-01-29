
def decode(data):
    print("decoding")
    datastr = ''.join([chr(b) for b in data])  # convert bytearray to string
    
    return datastr