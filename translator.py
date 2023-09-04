# communicate with an arduino board via serial port

import serial
import time
import sys
import os

# serial port
port = 'COM4'
baud = 115200

# open serial port
ser = serial.Serial(port, baud, timeout=1)

# read from serial port
def read():
    return ser.readline()

# write to serial port
def write(msg):
    ser.write(msg)

# close serial port
def close():
    ser.close()

# main
def main():
    print('Starting translator...')
    time.sleep(5)
    ser.setDTR(False)
    time.sleep(1)
    ser.flushInput()
    ser.setDTR(True)
    cont = True
    print("finished booting")
    try:
        while cont:
            time.sleep(0.1)
            write(b'1')
            print("wrote to arm")
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        cont = False
        close()
        sys.exit(0)


main()