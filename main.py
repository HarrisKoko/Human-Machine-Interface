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

def send_to_arm(max, min, val, letter):
    # convert val to a value between 0 and 180 using the range [min, max]
    # send the value to the arm
    if(max == min):
        return
    range = abs(max - min)
    new_val = abs(val - min) / range * 180
    print(max, min, val, int(new_val))
    ascii_num = chr(int(new_val))
    send_byte(letter, ascii_num)

def main():
    print("starting arm...")
    threading.Thread(target=start_arm).start()
    print("waiting for arm to boot...")
    time.sleep(30)
    print("arm booted")
    # first resolve an EEG stream on the lab network
    print("looking for an GYRO stream...")
    streams = resolve_stream('type', 'GYRO')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])
    run = True
    data1 = [0]
    data2 = [0]
    data3 = [0]
    sum1 = [0]
    sum2 = [0]
    sum3 = [0]
    max_and_minx = (0,0)
    max_and_miny = (0,0)
    max_and_minz = (0,0)
    old_time = 0
    old_time_write = 0
    while run:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        #print(timestamp, sample)
        override_val = 10
        if sample[0] < override_val and sample[0] > -override_val:
            sample[0] = 0
        if sample[1] < override_val and sample[1] > -override_val:
            sample[1] = 0
        if sample[2] < override_val and sample[2] > -override_val:
            sample[2] = 0
        val = quad(integrand, old_time, timestamp, args=(data1[len(data1)-1], sample[0]))
        sum1.append(sum1[len(sum1)-1] + val[0])
        val = quad(integrand, old_time, timestamp, args=(data2[len(data2)-1], sample[1]))
        sum2.append(sum2[len(sum2)-1] + val[0])
        val = quad(integrand, old_time, timestamp, args=(data3[len(data3)-1], sample[2]))
        sum3.append(sum3[len(sum3)-1] + val[0])
        data1.append(sample[0])
        data2.append(sample[1])
        data3.append(sample[2])

        if(sum1[len(sum1) - 1] > max_and_minx[0]):
            max_and_minx = (sum1[len(sum1) - 1], max_and_minx[1])
        if(sum1[len(sum1) - 1] < max_and_minx[1]):
            max_and_minx = (max_and_minx[0], sum1[len(sum1) - 1])
        
        if(sum2[len(sum2) - 1] > max_and_miny[0]):
            max_and_miny = (sum2[len(sum2) - 1], max_and_miny[1])
        if(sum2[len(sum2) - 1] < max_and_miny[1]):
            max_and_miny = (max_and_miny[0], sum2[len(sum2) - 1])
        
        if(sum3[len(sum3) - 1] > max_and_minz[0]):
            max_and_minz = (sum3[len(sum3) - 1], max_and_minz[1])
        if(sum3[len(sum3) - 1] < max_and_minz[1]):
            max_and_minz = (max_and_minz[0], sum3[len(sum3) - 1])

        #if(len(data1) > 1):
            #sum1.append(1/2 * (data1[len(data1) - 2] + data1[len(data1) - 1]) * (timestamp - old_time))
            #sum2.append(1/2 * (data1[len(data1) - 2] + data1[len(data1) - 1]) * (timestamp - old_time))
            #sum3.append(1/2 * (data1[len(data1) - 2] + data1[len(data1) - 1]) * (timestamp - old_time))
        old_time = timestamp
        #detect a keypress and set run to false
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print("key pressed")
            run = False
        
        # only send_to_arm every 1/2 second
        if(timestamp - old_time_write > 0.2):
            send_to_arm(max_and_minz[0], max_and_minz[1], sum3[len(sum3) - 1], 'D')
            old_time_write = timestamp

    #plot
    # plt.plot(data1)
    # plt.plot(data2)
    # plt.plot(data3)
    #plt.show()
    # plt.plot(sum1)
    # plt.plot(sum2)
    plt.plot(sum3)
    plt.show()

def handle_signal(signum, frame):
    print(f'handling signal {signum}')
    # do cleanup
    close()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    main()