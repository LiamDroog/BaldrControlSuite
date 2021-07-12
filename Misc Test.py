from LaserTrigger import shoot
import time
import multiprocessing as mp
import matplotlib.pyplot as plt
import numpy as np
from ClockClass import Clock
import os
import sys

def main():
    st = time.time()
    delayarr = np.arange(0.5, 10.5, 0.5)
    delaylen = len(delayarr)
    arr = list(i + 1 for i in range(100))
    arrlen = len(arr)
    totaliter = arrlen*delaylen
    printProgressBar(0, totaliter, prefix='Progress', suffix='Complete')
    iter = 1

    results = {}
    for rate in delayarr:
        r_arr = []
        for i in arr:
            iter += 1
            prefix = 'Current Rate: ' + str(rate) + ' Hz'
            printProgressBar(iter, totaliter, prefix=prefix, suffix='Complete')
            c = Clock(rate)
            st2 = time.time()
            for k in range(10):
                c.sleep()
            end = time.time() - st2
            r_arr.append((end - ((1 / rate) * 10)) / ((1 / rate) * 10) * 100)
        results[rate] = np.mean(r_arr)

    with open('simresults.txt', 'w') as f:
        for item, value in results.items():
            r = 'Rep rate: ' + str(item) + ' Percent Error: ' + str(value)[:5] + '\n'
            f.write(r)
    print('Time taken in outer shell: ', str(time.time() - st)[:6], 's')
    # print('Mean percent error over 1000 shots: ', np.mean(r_arr))
    # plt.plot(arr, r_arr)
    # plt.xlabel('Shot Group (10/group)')
    # plt.ylabel('Percent Error (%)')
    # plt.axhline(y=np.mean(r_arr), color='r')
    # plt.show()


def sleep_sim():
    arr = np.arange(0.05, 5, 0.05)
    l = len(arr)
    err = []
    printProgressBar(0, l, prefix='Progress', suffix='Complete')
    for i, j in enumerate(arr):
        os.system('cls')
        printProgressBar(i + 1, l, prefix='Progress', suffix='Complete')
        # print(str((i/l)*100)[:5], '% complete')
        st = time.time()
        time.sleep(j)
        end = time.time() - st
        err.append(((end - j) / j) * 100)
    plt.plot(arr, err)
    plt.xlabel('time.sleep() delay (s)')
    plt.ylabel('Percent Error (%)')
    plt.show()


def printProgressBar(iteration, total, prefix='', suffix='', decimals=2, length=80, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    # print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')

    # Print New Line on Complete
    if iteration == total:
        print()

def printProgressBarheader(header):
    sys.stdout.write(f'\r{header}')
    sys.stdout.write('\n')


if __name__ == '__main__':
    x = []
    y = []
    with open('simresults.txt', 'r') as f:
        for i in f:
            t = i.rstrip().split(';')
            x.append(float(t[0].split(':')[-1].strip()))
            y.append(float(t[1].split(':')[-1].strip()))

    plt.plot(x, y)
    plt.ylabel('Percent Error')
    plt.xlabel('Repetition Rate (hz)')
    plt.axis([max(x), min(x), min(y), max(y)])
    plt.show()

    # with open('Config/ControlConfig.cfg', 'r') as f:
    #     loadingText = []
    #     for i in f.readlines():
    #         loadingText.append(i.rstrip())
    #     import random
    #     for i in range(5):
    #         print(loadingText.pop(random.randint(0, len(loadingText) - 1)))
    #         for i in range(100):
    #             time.sleep(random.uniform(0.0001, 0.025))
    #             printProgressBar(i+1, 100, prefix='Progress')
