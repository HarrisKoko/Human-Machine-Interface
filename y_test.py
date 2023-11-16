# load data from y.csv
import csv
import matplotlib.pyplot as plt
from scipy.integrate import quad

def integrand(x, a, b):
    return a*x**2 + b

def load_data():
    # Specify the path to your CSV file
    csv_file_path = 'y.csv'
    time_file_path = 'time.csv'
    data = []
    timestamps = []
    filter = 0
    # Open the CSV file in read mode
    with open(time_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            for item in row:
                timestamps.append(float(item))
    with open(csv_file_path, 'r') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            for item in row:
                if float(item) > filter or float(item) < (-1 * filter):
                    data.append(float(item))
                else:
                    data.append(0)
    old_time = timestamps[0]
    sums = [0]
    print(len(timestamps))
    print(len(data))
    for i in range(1,len(timestamps)):
        val = 1/2 * (data[i] + data[i-1]) * (timestamps[i] - old_time)
        #val = quad(integrand, old_time, timestamps[i], args=(data[i-1], data[i]))
        #subtract the line containing (0,0) and (15,6) from the data
        sums.append(sums[i-1] + val)
        old_time = timestamps[i]

    sums2 = [0]
    old_time = timestamps[0]
    for i in range(1,len(timestamps)):
        val = 1/2 * (sums[i] + sums[i-1]) * (timestamps[i] - old_time)
        #val = quad(integrand, old_time, timestamps[i], args=(data[i-1], data[i]))
        #subtract the line containing (0,0) and (15,6) from the data
        sums2.append(sums2[i-1] + val)
        old_time = timestamps[i]

    for i in range(len(sums)):
        sums[i] = sums[i] - (10/3.1) * timestamps[i]

    plt.plot(timestamps, sums)
    #plt.plot(timestamps, data)
    plt.show()

load_data()