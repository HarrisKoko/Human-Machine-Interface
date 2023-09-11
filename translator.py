# communicate with an arduino board via serial port

import serial
import time
import sys
import os
from flask import Flask
from flask import request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'csv'

# serial port
port = 'COM4'
baud = 115200

cont = False

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

#translate a number on a 0 to 1 scale to a number on a 0 to 180 scale
def translate(num):
    return num * 180

#serial communication protocol
# A = base; B = shoulder; C = elbow; D = wrist vert; E = wrist rot; F = gripper
# protocol should send a letter followed by a number from 0 to 100

def send_byte(letter, num):
    write(letter.encode())
    write(str(num).encode())

# main
def main():
    print('Starting translator...')
    time.sleep(5)
    ser.setDTR(False)
    time.sleep(1)
    ser.flushInput()
    ser.setDTR(True)
    global cont
    cont = True
    print("finished booting")
    # try:
    #     while cont:
    #         time.sleep(0.1)
    #         send_byte('A', 67)
    #         print("wrote to arm")
    # except KeyboardInterrupt:
    #     print("KeyboardInterrupt")
    #     cont = False
    #     close()
    #     sys.exit(0)

# load the csv and read each line 
def load_csv(filename):
    with open(filename, 'r') as f:
        for line in f:
            translate(line)
            send_byte('A', line)

# create a route that accepts and saves a csv file
@app.route('/csv/<filename>', methods=['POST'])
def upload_csv(filename):
    # save the file
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'file uploaded successfully'

main()