# communicate with an arduino board via serial port

import serial
import time
import sys
import os

# serial port
port = '/dev/ttyACM0'
baud = 9600

# open serial port
ser = serial.Serial(port, baud, timeout=1)

# wait for arduino to boot
time.sleep(2)

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
if __name__ == '__main__':
    ser.setDTR(False)
    time.sleep(1)
    ser.flushInput()
    ser.setDTR(True)
    time.sleep(2)
    while True:
        try:
            sleep(1)
            write('1')
            print(read())
        except KeyboardInterrupt:
            close()
            sys.exit()