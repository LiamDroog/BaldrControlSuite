import PySpin
import os
import sys
import numpy as np


class GetBFSCameras:
    def __init__(self):
        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        self.cam_num = self.cam_list.GetSize()

        if self.cam_num == 0:
            self.cam_list.Clear()
            self.system.ReleaseInstance()
            print('no cameras!')
            return
        self.cam_dict = {}
        for i in self.cam_list:
            self.cam_dict[i.TLDevice.DeviceSerialNumber.ToString()] = i

    def releaseSystem(self):
        self.cam_list.Clear()
        self.system.ReleaseInstance()

    def getCameras(self):
        return self.cam_dict


class BFSTrigger:
    def __init__(self, camera):
        self.cam = camera
        self.triggermode = 1  # software trigger
        self.image_number = 1
        self.image_result = None
        self.nodemap_tldevice = self.cam.GetTLDeviceNodeMap()
        self.CamProperties = {}

    def triggerConfig(self):
        if self.cam.TriggerMode.GetAccessMode() != PySpin.RW:
            print('Unable to disable trigger mode (node retrieval). Aborting...')
            return False

        self.cam.TriggerMode.SetValue(PySpin.TriggerMode_Off)

        # Set TriggerSelector to FrameStart
        # For this example, the trigger selector should be set to frame start.
        # This is the default for most cameras.
        if self.cam.TriggerSelector.GetAccessMode() != PySpin.RW:
            print('Unable to get trigger selector (node retrieval). Aborting...')
            return False

        self.cam.TriggerSource.SetValue(PySpin.TriggerSelector_FrameStart)

        # Select trigger source
        # The trigger source must be set to hardware or software while trigger
        # mode is off.
        if self.cam.TriggerSource.GetAccessMode() != PySpin.RW:
            print('Unable to get trigger source (node retrieval). Aborting...')
            return False

        if self.triggermode == 1:
            self.cam.TriggerSource.SetValue(PySpin.TriggerSource_Software)
            # print('Trigger source set to software...')
        elif self.triggermode == 2:
            self.cam.TriggerSource.SetValue(PySpin.TriggerSource_Line0)
            # print('Trigger source set to hardware...')

            # Turn trigger mode on
            # Once the appropriate trigger source has been set, turn trigger mode
            # on in order to retrieve images using the trigger.
        self.cam.TriggerMode.SetValue(PySpin.TriggerMode_On)

    def trigger(self):
        """
        This function acts as the body of the example; please see NodeMapInfo example
        for more in-depth comments on setting up cameras.

        :param cam: Camera to run on.
        :type cam: CameraPtr
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            # Configure trigger
            if self.triggerConfig() is False:
                return False

            # Acquire images
            imagedata = self.acquire_images()

            # Reset trigger
            self.reset_trigger()


        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False
        return imagedata

    def deinit(self):
        self.cam.DeInit()

    def init(self):
        self.cam.Init()

    def reset_trigger(self):
        """
        This function returns the camera to a normal state by turning off trigger mode.

        :param cam: Camera to acquire images from.
        :type cam: CameraPtr
        :returns: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            result = True
            # Ensure trigger mode off
            # The trigger must be disabled in order to configure whether the source
            # is software or hardware.
            if self.cam.TriggerMode.GetAccessMode() != PySpin.RW:
                print('Unable to disable trigger mode (node retrieval). Aborting...')
                return False

            self.cam.TriggerMode.SetValue(PySpin.TriggerMode_Off)

            # print('Trigger mode disabled...')

        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            result = False

        return result

    def acquire_images(self):
        """
        This function acquires and saves 10 images from a device.
        Please see Acquisition example for more in-depth comments on acquiring images.

        :param cam: Camera to acquire images from.
        :type cam: CameraPtr
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        try:
            result = True

            # Set acquisition mode to continuous
            if self.cam.AcquisitionMode.GetAccessMode() != PySpin.RW:
                print('Unable to set acquisition mode to continuous. Aborting...')
                return False

            self.cam.AcquisitionMode.SetValue(PySpin.AcquisitionMode_Continuous)
            # print('Acquisition mode set to continuous...')

            #  Begin acquiring images
            self.cam.BeginAcquisition()

            # print('Acquiring images...')

            # Get device serial number for filename
            device_serial_number = ''
            if self.cam.TLDevice.DeviceSerialNumber.GetAccessMode() == PySpin.RO:
                device_serial_number = self.cam.TLDevice.DeviceSerialNumber.GetValue()

                # print('Device serial number retrieved as %s...' % device_serial_number)

            # Retrieve, convert, and save images
            try:

                #  Retrieve the next image from the trigger
                self.cam.TriggerSoftware.Execute()

                #  Retrieve next received image
                image_result = self.cam.GetNextImage(1000)

                #  Ensure image completion
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())

                else:
                    imagedata = image_result.GetNDArray()
                    #  Release image
                    image_result.Release()

            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False

            # End acquisition
            self.cam.EndAcquisition()
            return imagedata


        except PySpin.SpinnakerException as ex:
            print('Error: %s' % ex)
            return False

    def getDeviceParams(self):
        if self.cam.TLDevice.DeviceSerialNumber.GetAccessMode() == PySpin.RO:
            self.CamProperties['Device serial number'] = self.cam.TLDevice.DeviceSerialNumber.ToString()
        # Print device display name
        if PySpin.IsReadable(self.cam.TLDevice.DeviceDisplayName):
            self.CamProperties['Device display name'] = self.cam.TLDevice.DeviceDisplayName.ToString()

        if self.cam.ExposureTime.GetAccessMode() == PySpin.RO or self.cam.ExposureTime.GetAccessMode() == PySpin.RW:
            self.CamProperties['Exposure time'] = self.cam.ExposureTime.ToString()

        # Print black level
        if PySpin.IsReadable(self.cam.BlackLevel):
            self.CamProperties['Black level'] = self.cam.BlackLevel.ToString()

        # Print height
        if PySpin.IsReadable(self.cam.Height):
            self.CamProperties['Height'] = self.cam.Height.ToString()

        if PySpin.IsReadable(self.cam.Gain):
            self.CamProperties['Gain'] = self.cam.Gain.ToString()

        if PySpin.IsReadable(self.cam.Gamma):
            self.CamProperties['Gamma'] = self.cam.Gamma.ToString()

        return self.CamProperties

    def getSerialNumber(self):
        if self.cam.TLDevice.DeviceSerialNumber.GetAccessMode() == PySpin.RO:
            return self.cam.TLDevice.DeviceSerialNumber.ToString()


