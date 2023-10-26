# create a method that reads a csv file the is provided by the user

#the csv will be an array that contains numbers from 0 to 1

import random
import time

import requests


data = []

#create a fake csv using randomly generated numbers
def create_csv():
    # creating csv
    for i in range(100):
        data.append(random.random())
    return

#read the csv file and send the numbers to the arm

# Path: translator.py

def read_csv():
    # read from the data array, 0 cooresponds to 10 and 1 cooresponds to 73
    for i in data:
        val = i * 63 + 10
        val = int(val)
        val2 = 180 * i
        val2 = int(val2)
        print("Sending value: " + str(val))
        print("Sending value2: " + str(val2))
        # send a get request to the localhost followed by /C/val
        # this will send the value to the arm
        requests.get('http://localhost:5000/F/' + str(val))
        print("req 1 done")
        requests.get('http://localhost:5000/D/' + str(val2))
        print("req 2 done")

        # random int between 0 and 180
        val3 = random.randint(0, 180)

        requests.get('http://localhost:5000/B/' + str(val3))
        print("req 3 done")

        time.sleep(5)
    return

create_csv()
read_csv()