import PySpin
import matplotlib.pyplot as plt
import PIL
import keyboard


class BFSCam:

    def __init__(self, cam):
        """
        I have no idea what the heck all this is for.
        :param cam: Pointer to target camera
        """
        self.cam = cam
        self.cam.Init()
        self.nodemap = self.cam.GetNodeMap()
        self.sNodemap = self.cam.GetTLStreamNodeMap()
        self.node_bufferhandling_mode = PySpin.CEnumerationPtr(self.sNodemap.GetNode('StreamBufferHandlingMode'))
        self.node_newestonly = self.node_bufferhandling_mode.GetEntryByName('NewestOnly')
        self.node_newestonly_mode = self.node_newestonly.GetValue()
        self.node_bufferhandling_mode.SetIntValue(self.node_newestonly_mode)
        self.node_acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
        self.node_acquisition_mode_continuous = self.node_acquisition_mode.GetEntryByName('Continuous')
        self.acquisition_mode_continuous = self.node_acquisition_mode_continuous.GetValue()
        self.node_acquisition_mode.SetIntValue(self.acquisition_mode_continuous)
        self.isLiveOut = False
        self.beginAquisition()

    def beginAquisition(self):
        self.cam.BeginAcquisition()

    def stopAquisition(self):
        self.cam.EndAcquisition()

    def deInit(self):
        self.stopAquisition()
        self.cam.DeInit()
        del self.cam
        return

    def getImage(self):
        image = self.cam.GetNextImage()
        #imagedata = image.GetNDArray()
        image.Release()

        return image

    def liveOut(self):
        self.isLiveOut = True
        fig = plt.figure(1)
        fig.canvas.mpl_connect('close_event', self.__onExitLiveView)
        while self.isLiveOut:
            image = self.cam.GetNextImage()
            imagedata = image.GetNDArray()
            plt.imshow(imagedata, cmap='gray')
            plt.pause(0.001)
            plt.clf()
            image.Release()
            if keyboard.is_pressed('Enter'):
                self.stopLiveOut()

    def liveOut_withLineout(self):
        # needs optimixation yo
        self.isLiveOut = True
        fig, axs = plt.subplots(2)
        while self.isLiveOut:
            image = self.cam.GetNextImage()
            imagedata = image.GetNDArray()
            axs[1].plot(self.lineout(imagedata))
            axs[0].imshow(imagedata, cmap='gray')
            #plt.imshow(imagedata, cmap='gray')
            plt.pause(0.001)
            plt.cla()
            image.Release()
            if keyboard.is_pressed('Enter'):
                self.stopLiveOut()

    def stopLiveOut(self):
        self.isLiveOut = False

    def lineout(self, data):
        arr = []
        for i in range(len(data[0])):
            avg = 0
            for j in data:
                avg += j[i]
            avg = avg / len(data[0])
            arr.append(avg)
        return arr

    def __onExitLiveView(self, event):
        self.isLiveOut = False
