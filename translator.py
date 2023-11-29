# communicate with an arduino board via serial port

import random
import serial
import time
import sys
import os
from flask import Flask
from flask import request
import signal
import threading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'csv'

sleep_time = 0.2

# serial port
port = "COM4"
baud = 9600

cont = False

def init_arm():
    global ser
    # open serial port
    print("opening serial port")
    ser = serial.Serial(port, baud, writeTimeout=0)
    print("opened serial port")
    time.sleep(2)
    ser.setDTR(False)
    time.sleep(2)
    print("flushing input")
    ser.flushInput()
    ser.setDTR(True)
    print("Done")

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
    return round(num * 180)

#serial communication protocol
# A = base; B = shoulder; C = elbow; D = wrist vert; E = wrist rot; F = gripper
# protocol should send a letter followed by a number from 0 to 100

def send_byte(letter, num):
    # print("sending byte")
    # print(num)
    encoded_num = num.encode()
    if(sys.getsizeof(encoded_num) > 34):
        #trim off the first byte
        #print("trimming")
        encoded_num = encoded_num[1:]
        #print(encoded_num)
    write(letter.encode())
    write(encoded_num)

def listen():
    while(True):
        print((read()))
        time.sleep(sleep_time)

# def communicate():
#     # while(True):
#     #     random_pos()
#     print()

# main
def thing():
    print('Starting translator...')
    time.sleep(2)
    ser.setDTR(False)
    time.sleep(2)
    ser.flushInput()
    ser.setDTR(True)
    global cont
    cont = True
    print("finished booting")
    print("running loop")

    test = threading.Thread(target=listen)
    test.start()
    # time.sleep(10)
    # test2 = threading.Thread(target=communicate)
    # test2.start()

# random position generator
def random_pos():
    val = int(random.random() * 73 + 10)
    val2 = int(random.random() * 180)
    val3 = int(random.random() * 180)

    print("Sending value: " + str(val))
    print("Sending value2: " + str(val2))
    print("Sending value3: " + str(val3))

    get('F', val)
    time.sleep(0.5)
    print("sent byte 1")
    get('E', val2)
    print("sent byte 2")
    get('D', val3)
    print("sent byte 3")
    time.sleep(0.5)

# load the csv and read each line 
def load_csv(filename):
    with open(filename, 'r') as f:
        for line in f:
            #if line.replace(".", "").isdigit():
            out = translate(float(line))
            ascii_num = chr(int(out))
            rand = random.random()
            # if rand < 0.25:
            #     ch = 'F'
            # elif rand < 0.5:
            #     ch = 'E'
            # elif rand < 0.75:
            #     ch = 'D'
            # else:
            #     ch = 'C'
            ch = 'F'
            send_byte(ch, ascii_num)
            time.sleep(sleep_time)

# create a route that accepts and saves a csv file
@app.route('/csv/<filename>', methods=['POST'])
def upload_csv(filename):
    # save the file
    f = request.files['file']
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'file uploaded successfully'

@app.route('/load/<filename>', methods=['GET'])
def load(filename):
    load_csv(filename)
    return 'loaded'

# GET - takes in a letter A through E as well as a number
@app.route('/<letter>/<num>', methods=['GET'])
def get(letter, num):
    print("run")
    ascii_num = chr(int(num))
    send_byte(letter, ascii_num)
    return 'sent'

def handle_signal(signum, frame):
    print(f'handling signal {signum}')
    # do cleanup
    close()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_signal)

init_arm()
thing()