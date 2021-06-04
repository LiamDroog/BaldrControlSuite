import os

import matplotlib.pyplot as plt
import numpy as np
from datetime import date

from SimpleFLIR import Camera


class CameraNotConnected(Exception):
    pass


class RunBlackFlyCamera:
    def __init__(self, camserial, date, filenum):
        # camserial: camera serial number
        # filenum: starting number for files
        # instantiate camera
        try:
            self.cam = Camera(camserial)
        except:
            raise CameraNotConnected('Camera ' + camserial + ' not connected.')

        self.camserial = camserial
        self.camName = self.cam.getDeviceName()
        self.filenum = filenum
        self.datafilename = self.camserial + '_shotdata_' + '0' * (4 - len(str(self.filenum))) + str(filenum) + '.npy'
        self.metadatafilename = self.camserial + '_shotmetadata_' + '0' * (4 - len(str(self.filenum))) + str(
            filenum) + '.npy'

        # set file directory
        self.filepath = 'TempDataFiles/' + '/' + self.camserial + '/'

        if not os.path.exists(self.filepath):
            os.makedirs(self.filepath)

        # initialize camera
        self.cam.init()

    def adjust(self, target, value):
        self.cam.__setattr__(target, value)

    def handleTrigger(self):
        self.__saveData(self.cam.get_array())
        self.filenum += 1

    def __getShotMetadata(self):
        return self.cam.getDeviceParams()

    def __saveData(self, data):
        self.datafilename = self.camserial + '_shotdata_' + '0' * (4 - len(str(self.filenum))) + str(
            self.filenum) + '.npy'
        returndict = {}
        returndict['diagnosticname'] = self.camName + ' Serial: ' + self.camserial
        returndict['targetfile'] = self.filenum
        returndict['data'] = data
        returndict['metadata'] = self.__getShotMetadata()
        np.save(self.filepath + self.datafilename, returndict)

    def start(self):
        self.cam.start()

    def stop(self):
        self.cam.stop()

    def close(self):
        self.cam.close()

    def liveView(self):
        self.isLiveOut = True
        self.cam.configliveout()
        fig = plt.figure(1)
        fig.canvas.mpl_connect('close_event', self.__closeLiveView)

        while self.isLiveOut:
            image = self.cam.get_array()
            plt.imshow(image, cmap='gray')
            plt.pause(0.001)
            plt.clf()

    def __closeLiveView(self, event):
        self.isLiveOut = False


if __name__ == '__main__':
    today = date.today()
    date = today.strftime("%b-%d-%Y")
    camera = RunBlackFlyCamera('19129388', date, 1)
    camera.start()
    for i in range(10):
        camera.handleTrigger()
    camera.stop()
    camera.close()
