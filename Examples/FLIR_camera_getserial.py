"""
##################################################
Demonstrates how to obtain a list of all connected
blackfly FLIR camera serial numbers
##################################################
# Author:   Liam Droog
# Email:    droog@ualberta.ca
# Year:     2021
# Version:  V.1.0.0
##################################################
"""
from SimpleFLIR import GetBFSCameras

if __name__ == '__main__':
    cams = GetBFSCameras()
    camList = cams.getCameras()
    print(camList)

