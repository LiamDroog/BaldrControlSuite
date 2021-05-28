import PySpin
import matplotlib.pyplot as plt
from FLIRLib import BFSCam
import time
import keyboard


def main():

    system = PySpin.System.GetInstance()
    cam = system.GetCameras()[0]
    camera = BFSCam(cam)
    camera.beginAquisition()
    data = camera.getImage()
    camera.stopAquisition()
    camera.deInit()

    # plt.imshow(data, cmap='gray')
    # plt.show()

    #system.ReleaseInstance()


    # system = PySpin.System.GetInstance()


#     cam = system.GetCameras()[0]
#
#     global continue_recording
#     continue_recording = True
#
#     cam.Init()
#
#     nodemap = cam.GetNodeMap()
#
#     sNodemap = cam.GetTLStreamNodeMap()
#
#     node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))
#
#     node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
#
#     node_newestonly_mode = node_newestonly.GetValue()
#
#     node_bufferhandling_mode.SetIntValue(node_newestonly_mode)
#
#     node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
#
#     node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
#
#     acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
#
#     node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
#
#     cam.BeginAcquisition()
#     fig = plt.figure(1)
#     fig.canvas.mpl_connect('close_event', handle_close)
#
#     image_result = cam.GetNextImage(1000)
#     image_data = image_result.GetNDArray()
#     plt.imshow(image_data, cmap='gray')
#     plt.show()
#     # plt.pause(0.001)
#     # plt.clf()
#     image_result.Release()
#     cam.EndAcquisition()
#     cam.DeInit()
#     del cam
#     system.ReleaseInstance()

#
#
# def handle_close(evt):
#     """
#     This function will close the GUI when close event happens.
#
#     :param evt: Event that occurs when the figure closes.
#     :type evt: Event
#     """
#
#     global continue_recording
#     continue_recording = False

if __name__ == '__main__':
    main()
