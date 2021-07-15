"""
##################################################
Demonstrates how to utilize the BlackFlyCamera
##################################################
# Author:   Liam Droog
# Email:    droog@ualberta.ca
# Year:     2021
# Version:  V.1.0.0
##################################################
"""
from BlackFlyCameraClass import RunBlackFlyCamera
from PIL import Image

if __name__ == '__main__':
    ###########################
    serial = '19129388'
    shotNum = 5
    LiveView = True
    ###########################

    # instantiate camera
    bfs = RunBlackFlyCamera(serial, shotNum)
    # begin aquisition
    if LiveView:
        # doesn't need a cam.start() call, but needs a stop() call
        bfs.adjust('GainAuto', 'Off')
        bfs.adjust('ExposureAuto', 'Off')
        bfs.adjust('ExposureTime', 5000)
        bfs.liveView()
    else:
        bfs.adjust('GainAuto', 'Off')
        bfs.adjust('ExposureAuto', 'Off')
        bfs.adjust('ExposureTime', 5000)
        bfs.start()
        data = bfs.get_image_array()
        im = Image.fromarray(data, 'L')
        #im.show()
        im.save('FLIR' + str(shotNum) + '.bmp')
    # stop aquisition
    bfs.stop()
    # close camera
    bfs.close()
    del bfs