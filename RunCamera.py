import os
from autoBFSCam import RunBlackFlyCamera, ListCameras
import multiprocessing


def main():
    # get list of connected cameras
    available_camera_list = ListCameras().get()
    camera_list = []
    os.system('cls')

    # make physicists cringe with variable name
    hbar = '#' * 80
    print(hbar)

    # check to see if there are no cameras connected
    if not available_camera_list:
        print('\033[31mNo cameras connected. Aborting...\033[0m')
        return

    print('Available Cameras:')
    for i in available_camera_list:
        print(i)

    # ensure connected cameras match expected cameras
    for i in range(len(camera_serial_list)):
        if camera_serial_list[i] not in available_camera_list:
            print('\033[31m' + 'Camera ' + camera_serial_list[i] + ' is not connected.\033[0m')
            camera_serial_list.pop(i)

    # get filenumber
    print('Getting file number from directory:', hdf5Directory)
    filenumber = check_filenum()
    print('Set file number to ' + str(filenumber) + '.')
    print(hbar)
    for i in camera_serial_list:
        print(('Initializing camera ' + str(i) + '.').center(80))
        camera_list.append(RunBlackFlyCamera(i, filenumber))
    print(hbar, '\n')
    # todo: multiprocessing thread for each camera to handle
    #       saving images to
    camera_list[0].start()
    camera_list[0].printInfo()
    print(hbar)

    for i in camera_list:
        print(('Closing camera ' + str(i.camserial) + '.').center(80))
        i.close()
    print(hbar)


def check_filenum():
    owd = os.getcwd()
    try:
        os.chdir(hdf5Directory)
        dirs = [file for file in os.listdir()
                if os.path.isfile(file)]
        if not dirs:
            shotnum = 0
        else:
            for i in range(len(dirs)):
                if dirs[i][-5:] != '.hdf5':
                    dirs.pop(i)
            # now we have a list of all hdf5 files
            dirs.sort(reverse=True)
            lastfile = dirs[0]
            lf1 = lastfile[:-5].split('shot')[1]
            for i in range(len(str(lf1))):
                if lf1[i] != '0':
                    shotnum = int(lf1[i:])
    finally:
        os.chdir(owd)
        return shotnum




if __name__ == '__main__':
    # todo: file number start at 0, need to start at whatever number
    #   or, add 'new folder' button to controlHub for each run that
    #   resets to zero
    # INPUT SERIAL NUMBERS
    # INPUT DIRECTORY CONTAINING HDF5 SHOT FILES
    # (THE ONE THAT HDF5Daemon.py WRITES TO VIA
    # ControlHub.py)
    # ######################
    camera_serial_list = ['19129388']
    hdf5Directory = 'C:/Users/Liam/PycharmProjects/BaldrControlHub py3.8/DataFiles/queue/'
    # ######################
    main()

