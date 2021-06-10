from FWHMFinder import get_fwhm, gauss
from PIL import Image
import numpy as np
import time
import matplotlib.pyplot as plt
import tkinter as tk
from BlackFlyCameraClass import RunBlackFlyCamera


class FocusingHelper:
    def __init__(self):
        self.window = tk.Tk(className='Focus Assist')
        self.window.geometry(
            '%dx%d+%d+%d' % (int(self.window.winfo_screenwidth() * 0.15), int(self.window.winfo_screenheight() * 0.15),
                             self.window.winfo_screenwidth() / 4,
                             self.window.winfo_screenheight() / 5))
        self.button = tk.Button(master=self.window, text='Press me!', command=self.takeimage)
        self.button.pack(expand=True, fill='both')
        self.bfs = RunBlackFlyCamera('19129388', 0)
        self.bfs.adjust('GainAuto', 'Off')
        self.bfs.adjust('ExposureAuto', 'Off')
        self.bfs.adjust('ExposureTime', 50)
        self.window.protocol("WM_DELETE_WINDOW", self.__on_closing)
        selfpxpitch = 4.8
        self.window.mainloop()

    def takeimage(self):
        self.bfs.start()
        im = self.bfs.get_image_array()
        self.analyze(im)
        self.bfs.stop()

    def analyze(self, dat):
        plt.clf()
        st = time.time()
        try:
            (fwhmx, fwhmy), (xopt, yopt) = get_fwhm(dat, rfactor=1, plot=False)
        except:
            print('Could not fit data')
            plt.text(0, -65, 'FWHM Values could not be obtained')
        else:

            meanval = np.mean(dat)
            print('Took ' + str(time.time() - st) + ' seconds.')
            print("fwhm x:", fwhmx, "->", fwhmx*self.pxpitch, 'micron')
            print("fwhm y:", fwhmy, "->", fwhmy*self.pxpitch, 'micron')
            print('Mean pixel value:', str(meanval))
            print('\n')
            plt.plot([xopt[1] - 0.5 * fwhmx, xopt[1] + 0.5 * fwhmx], [yopt[1], yopt[1]], c='black')
            plt.plot([xopt[1], xopt[1]], [yopt[1] - 0.5 * fwhmy, yopt[1] + 0.5 * fwhmy], c='black')
            plt.scatter([xopt[1]], [yopt[1]], c='black')
            plt.text(0, -65,
                     str("FWHM x: " + str(fwhmx)[:6] + " Pixels -> " + str(fwhmx * self.pxpitch)[:6] + ' micron '))
            plt.text(0, -15,
                     str("FWHM y: " + str(fwhmy)[:6] + " Pixels -> " + str(fwhmy * self.pxpitch)[:6] + ' micron '))

        plt.imshow(dat, cmap='Spectral')
        plt.xlabel('Pixel Number')
        plt.ylabel('Pixel Number')
        plt.colorbar()




        plt.show()

    def __on_closing(self):
        self.bfs.close()
        self.window.destroy()
if __name__ == '__main__':
    FocusingHelper()
