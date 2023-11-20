# read from the "Acc_recoding_2023-11-14-18.25.54.csv" file
# it contains data in the form of "timestamp, x, y, z" and has a header
# the data is in the form of a csv file
# plot it after reading it
import csv
import math
import time
import matplotlib.pyplot as plt
from pylsl import StreamInlet, resolve_stream
import msvcrt

# def plot_and_read():
#     # Specify the path to your CSV file
#     csv_file_path = 'ACC_recording_2023-11-14-18.25.54.csv'
#     datax = []
#     datay = []
#     dataz = []
#     timestamps = []
#     filter = 0
#     # Open the CSV file in read mode
#     with open(csv_file_path, 'r') as file:
#         # Create a CSV reader object
#         csv_reader = csv.reader(file)
#         #skip the first row
#         next(csv_reader)
#         # Iterate over each row in the CSV file
#         for row in csv_reader:
#             #print(row)
#             timestamps.append(float(row[0]))
#             datax.append(float(row[1]))
#             if float(row[2]) > filter or float(row[2]) < (-1 * filter):
#                 datay.append(float(row[2]))
#             else:
#                 datay.append(0)
#             dataz.append(float(row[3]))

#     #determine line of best fit for data y
#     #y = mx + b
#     m = (datay[699] - datay[0]) / (timestamps[699] - timestamps[0])
#     b = datay[0] - m * timestamps[0]
#     # for i in range(len(datay)):
#     #     datay[i] = datay[i] - (m * timestamps[i] + b)

#     # sums = [0]
#     # old_time = timestamps[0]
#     # for i in range(1,len(timestamps)):
#     #     val = 1/2 * (datay[i] + datay[i-1]) * (timestamps[i] - old_time)
#     #     sums.append(sums[i-1] + val)
#     #     old_time = timestamps[i]

#     #plt.plot(timestamps, datax)
#     plt.plot(datay)
#     #plt.plot(timestamps, dataz)
#     #plt.plot(timestamps, data)
#     plt.show()

channel1 = []
channel2 = []
channel3 = []
channel4 = []
channel5 = []
timestamps = []

def read():
    streams = resolve_stream('type', 'EEG')
    inlet = StreamInlet(streams[0])
    init_sample, init_timestamp = inlet.pull_sample()
    timestamp = init_timestamp
    while(timestamp - init_timestamp < 5):
        sample, timestamp = inlet.pull_sample()
        channel3.append(sample[2])
        

    plt.plot(channel3)
    plt.show()
    mx = max(channel3)
    mn = min(channel3)
    range = (mx - mn)
    avg = sum(channel3)/len(channel3)

    run = True
    print(avg)

    blink_time = init_timestamp

    while run:
        sample, timestamp = inlet.pull_sample()
        #print(timestamp, sample)
        timestamps.append(timestamp)
        channel1.append(sample[0])
        channel2.append(sample[1])
        channel3.append(sample[2])
        channel4.append(sample[3])
        channel5.append(sample[4])
        if((sample[2] > avg + range or sample[2] < avg - range) and timestamp - blink_time > 1):
            blink_time = timestamp
            print("blink")

        if msvcrt.kbhit():
            key = msvcrt.getch()
            print("key pressed")
            run = False

read()
plt.plot(channel1)
plt.show()
plt.plot(channel2)
plt.show()
plt.plot(channel3)
plt.show()
plt.plot(channel4)
plt.show()
plt.plot(channel5)
plt.show()