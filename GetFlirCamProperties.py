from BlackFlyCameraClass import RunBlackFlyCamera
import time
class getCamInfo:
    """
    This class will iterate through the camera to obtain relevant data and write to a dictionary for storage
    """
    def __init__(self, camera, file):
        self.cam = camera
        self.cam.start()
        self.cam.adjust('GainAuto', 'Off')
        self.cam.adjust('ExposureAuto', 'Off')
        self.cam.adjust('ExposureTime', 69)
        st = time.time()
        with open(file, 'r') as f:
            for i in f:
                j = i.split(':')[0]
                try:
                    print(j, ':', self.cam.get(j))
                except:
                    continue
        print('took %3.4f seconds' % (time.time() - st))


if __name__ == '__main__':
    x = RunBlackFlyCamera('19129388', 0)
    getCamInfo(x, 'Config/flir_cam_md_values.txt')
    x.close()