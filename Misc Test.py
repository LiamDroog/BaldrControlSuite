import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

def main():
    # x fit, y fit should just have fwhm center be centered on the sensor. height has to be manual tho
    d = {
        15  :   100,
        25  :   200,
        5   :   150

    }
    ad = {
        -2:4,
        -1:1,
        -0.5: 0.25,
        0:0,

        1:1,
        2:4
    }
    x = []
    y = []
    for key, val in sorted(d.items()):
        print(key, val)
        x.append(key)
        y.append(val)
    xi = np.linspace(x[0], x[-1])
    y = np.interp(xi, x, y)
    plt.scatter(xi, y)

    popt, _ = curve_fit(parabola, xi, y)
    print('vertex: (%d, %d)' % (popt[1], popt[2]))
    plt.plot(xi, parabola(xi, *popt))
    plt.show()


def parabola(x, a, b, c):
    return (a * (x-b)**2) + c


main()
