# read from the "Acc_recoding_2023-11-14-18.25.54.csv" file
# it contains data in the form of "timestamp, x, y, z" and has a header
# the data is in the form of a csv file
# plot it after reading it
import csv
import matplotlib.pyplot as plt

def plot_and_read():
    # Specify the path to your CSV file
    csv_file_path = 'ACC_recording_2023-11-14-18.25.54.csv'
    datax = []
    datay = []
    dataz = []
    timestamps = []
    filter = 0
    # Open the CSV file in read mode
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        #skip the first row
        next(csv_reader)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            #print(row)
            timestamps.append(float(row[0]))
            datax.append(float(row[1]))
            if float(row[2]) > filter or float(row[2]) < (-1 * filter):
                datay.append(float(row[2]))
            else:
                datay.append(0)
            dataz.append(float(row[3]))

    #determine line of best fit for data y
    #y = mx + b
    m = (datay[699] - datay[0]) / (timestamps[699] - timestamps[0])
    b = datay[0] - m * timestamps[0]
    for i in range(len(datay)):
        datay[i] = datay[i] - (m * timestamps[i] + b)

    sums = [0]
    old_time = timestamps[0]
    for i in range(1,len(timestamps)):
        val = 1/2 * (datay[i] + datay[i-1]) * (timestamps[i] - old_time)
        sums.append(sums[i-1] + val)
        old_time = timestamps[i]

    #plt.plot(timestamps, datax)
    plt.plot(datax)
    #plt.plot(timestamps, dataz)
    #plt.plot(timestamps, data)
    plt.show()

plot_and_read()