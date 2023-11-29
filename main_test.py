import msvcrt
from pylsl import StreamInlet, resolve_stream
from scipy.integrate import quad
from translator import send_byte, thing, init_arm, close
import threading
import time
import signal
import sys
import matplotlib.pyplot as plt

def integrand(x, a, b):
    return a*x**2 + b

def start_arm():
    init_arm()
    thing()

def send_to_arm(max, min, val, letter, inverse):
    # convert val to a value between 0 and 180 using the range [min, max]
    # send the value to the arm
    if(max == min):
        return
    range = abs(max - min)
    new_val = abs(val - min) / range * 180
    if inverse:
        new_val = 180 - new_val
    print(max, min, val, int(new_val))
    ascii_num = chr(int(new_val))
    send_byte(letter, ascii_num)

def determine_drift(timestamps, data):
    # determine the drift of the data
    # return the drift in the form (m, b)
    # where y = mx + b
    total_slope_sum = 0
    total_slope_count = 0
    for i in range(1, len(data)):
        if timestamps[i] - timestamps[i-1] > 0:
            total_slope_count += 1
            total_slope_sum += (data[i] - data[i-1]) / (timestamps[i] - timestamps[i-1])
    m = total_slope_sum / (total_slope_count - 1)
    b = data[0] - m * timestamps[0]
    print("approx: " + str((data[len(data) - 1] - data[0]) / (timestamps[len(timestamps) - 1] - timestamps[0])))

    return (m, b)

def calibrate_blink(inlet):
    eegInit_sample, eegInit_timestamp = inlet.pull_sample()
    eegTimestamps = [eegInit_timestamp]
    eegSamples = []
    while(eegTimestamps[len(eegTimestamps) - 1] - eegInit_timestamp < 5):
        eegSample, eegTimestamp = inlet.pull_sample()
        eegTimestamps.append(eegTimestamp)
        eegSamples.append(eegSample[2])
    mx = max(eegSamples)
    mn = min(eegSamples)
    rang = (mx - mn)
    avg = sum(eegSamples)/len(eegSamples)
    return (avg, rang)

def run_blink():
    eegStreams = resolve_stream('type', 'EEG')
    eegInlet = StreamInlet(eegStreams[0])
    print("calibrating blink, remain still for 5 seconds")
    calibration = calibrate_blink(eegInlet)
    print("calibrated blink")
    run = True
    full_grip = False
    while run:
        sample, timestamp = eegInlet.pull_sample()
        avg = calibration[0]
        range = calibration[1]
        if((sample[2] > avg + range or sample[2] < avg - range) and timestamp - blink_time > 1):
            blink_time = timestamp
            print("blink")
            full_grip = not full_grip
        
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print("key pressed")
            run = False

def calibrate(intlet):
    print("Remain still for 5 seconds")
    init_sample, init_timestamp = intlet.pull_sample()
    # eegInit_sample, eegInit_timestamp = eegInlet.pull_sample()
    timestamps = [init_timestamp]
    # eegTimestamps = [eegInit_timestamp]
    # eegSamples = []
    datax = [init_sample[0]]
    datay = [init_sample[1]]
    dataz = [init_sample[2]]
    sumx = [0]
    sumy = [0]
    sumz = [0]
    #store data to arrays
    while(timestamps[len(timestamps) - 1] - init_timestamp < 5):
        sample, new_timestamp = intlet.pull_sample()
        datax.append(sample[0])
        datay.append(sample[1])
        dataz.append(sample[2])
        timestamps.append(new_timestamp)
        # eegSample, eegTimestamp = eegInlet.pull_sample()
        # eegTimestamps.append(eegTimestamp)
        # eegSamples.append(eegSample[2])
    #retroactively integrate
    for i in range(1, len(datax)):
        valx = 1/2 * (datax[i] + datax[i-1]) * (timestamps[i] - timestamps[i-1])
        sumx.append(sumx[len(sumx)-1] + valx)
        valy = 1/2 * (datay[i] + datay[i-1]) * (timestamps[i] - timestamps[i-1])
        sumy.append(sumy[len(sumy)-1] + valy)
        valz = 1/2 * (dataz[i] + dataz[i-1]) * (timestamps[i] - timestamps[i-1])
        sumz.append(sumz[len(sumz)-1] + valz)
    timestamps.pop(0)
    print(timestamps)
    sumx.pop(0)
    sumy.pop(0)
    sumz.pop(0)
    #determine the respective drifts
    x_drift = determine_drift(timestamps, sumx)
    y_drift = determine_drift(timestamps, sumy)
    z_drift = determine_drift(timestamps, sumz)
    print(timestamps[len(timestamps) - 1] - timestamps[1])
    print(sumy[1], sumy[len(sumy) - 1])
    print(x_drift, y_drift, z_drift)
    # plt.plot(timestamps, sumy)
    # plt.show()
    # mx = max(eegSamples)
    # mn = min(eegSamples)
    # rang = (mx - mn)
    # avg = sum(eegSamples)/len(eegSamples)
    return (x_drift, y_drift, z_drift)

def main():
    print("starting arm...")
    threading.Thread(target=start_arm).start()
    print("waiting for arm to boot...")
    time.sleep(30)
    print("arm booted")
    # first resolve an GYRO stream on the lab network
    print("looking for an GYRO stream...")
    streams = resolve_stream('type', 'GYRO')
    print("resolving stream...")
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    threading.Thread(target=run_blink).start()
    #calibrate
    print("calibrating...")
    calibration = calibrate(inlet)
    print("calibrated")
    #wait for arm to boot
    
    run = True
    init_sample, init_timestamp = inlet.pull_sample()
    datax = [init_sample[0]]
    datay = [init_sample[1]]
    dataz = [init_sample[2]]
    timestamps = [init_timestamp]
    sumx = [0]
    sumy = [0]
    sumz = [0]
    max_and_minx = (0,0)
    max_and_miny = (0,0)
    max_and_minz = (0,0)
    old_time = init_timestamp
    # blink_time = init_timestamp
    old_time_write = 0

    # full_grip = False

    while run:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        #print(timestamp, sample)
        override_val = 10
        if sample[0] < override_val + calibration[0][0] and sample[0] > -override_val + calibration[0][0]:
            sample[0] = 0
        if sample[1] < override_val + calibration[1][0] and sample[1] > -override_val + calibration[1][0]:
            sample[1] = 0
        if sample[2] < override_val + calibration[2][0] and sample[2] > -override_val + calibration[2][0]:
            sample[2] = 0
        
        valx = quad(integrand, old_time, timestamp, args=(datax[len(datax)-1], sample[0]))
        sumx.append(sumx[len(sumx)-1] + valx[0])
        valx = valx[0] # - calibration[0][0] * (timestamp - old_time)

        valy = 1/2 * (datay[len(datay) - 1] + sample[1]) * (timestamp - old_time) 

        valy = valy # - calibration[1][0] * (timestamp - old_time)

        sumy.append(sumy[len(sumy)-1] + valy)

        valz = quad(integrand, old_time, timestamp, args=(dataz[len(dataz)-1], sample[2]))
        valz = valz[0] # - calibration[2][0] * (timestamp - old_time)

        sumz.append(sumz[len(sumz)-1] + valz)
        datax.append(sample[0])
        datay.append(sample[1])
        dataz.append(sample[2])
        timestamps.append(timestamp)

        if(sumx[len(sumx) - 1] > max_and_minx[0]):
            max_and_minx = (sumx[len(sumx) - 1], max_and_minx[1])
        if(sumx[len(sumx) - 1] < max_and_minx[1]):
            max_and_minx = (max_and_minx[0], sumx[len(sumx) - 1])
        
        if(sumy[len(sumy) - 1] > max_and_miny[0]):
            max_and_miny = (sumy[len(sumy) - 1], max_and_miny[1])
        if(sumy[len(sumy) - 1] < max_and_miny[1]):
            max_and_miny = (max_and_miny[0], sumy[len(sumy) - 1])
        
        if(sumz[len(sumz) - 1] > max_and_minz[0]):
            max_and_minz = (sumz[len(sumz) - 1], max_and_minz[1])
        if(sumz[len(sumz) - 1] < max_and_minz[1]):
            max_and_minz = (max_and_minz[0], sumz[len(sumz) - 1])

        old_time = timestamp
        #detect a keypress and set run to false
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print("key pressed")
            run = False
        

        # sample, timestamp = eegInlet.pull_sample()
        # avg = calibration[3][0]
        # range = calibration[3][1]
        # if((sample[2] > avg + range or sample[2] < avg - range) and timestamp - blink_time > 1):
        #     blink_time = timestamp
        #     print("blink")
        #     full_grip = not full_grip

        if(timestamp - old_time_write > 0.5):
            send_to_arm(max_and_minz[0], max_and_minz[1], sumz[len(sumz) - 1], 'D', True)
            send_to_arm(max_and_miny[0], max_and_miny[1], sumy[len(sumy) - 1], 'E', False)
            old_time_write = timestamp

    #plot
    # plt.plot(datax)
    # plt.plot(datay)
    plt.plot(dataz)
    plt.show()
    plt.plot(timestamps, sumy)
    plt.show()
    plt.plot(timestamps, sumz)
    plt.show()

def handle_signal(signum, frame):
    print(f'handling signal {signum}')
    # do cleanup
    close()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    main()