import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time


def main():
    st = time.time()
    filename = 'FLIR0.bmp'
    im = Image.open(filename)
    data = np.asarray(im)
    xdat = lineout_x(data)
    ydat = lineout_y(data)
    print('Took ' + str(time.time() - st) + ' seconds.')
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.plot(xdat)
    ax2.plot(ydat)
    plt.show()


def lineout_x(data):
    avg_arr = []
    for i in range(len(data)):
        total = 0
        for j in range(len(data[i])):
            total += data[i][j]
        avg_arr.append(total / len(data[i]))
    return normalize(avg_arr)


def lineout_y(data):
    avg_arr = []
    length = len(data)
    # assumes all sub arrays are the same shape - image is always 1280x1024 so this assumption is valid.
    for j in range(len(data[0])):
        total = 0
        for i in range(len(data)):
            total += data[i][j]
        avg_arr.append(total / length)
    return normalize(avg_arr)


def normalize(iarr):
    ret = []
    mx = max(iarr)
    mn = min(iarr)
    for i in iarr:
        ret.append(np.interp(i, [mn, mx], [0, 1]))
    return ret


if __name__ == '__main__':
    main()
