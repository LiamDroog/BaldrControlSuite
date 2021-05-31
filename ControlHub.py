import tkinter as tk
from tkinter import font, messagebox
from droogCNC import TwoAxisStage
from HDF5Browser import FileBrowser
import HDF5Methods as h5m
import serial.tools.list_ports
from ImageViewer import ImageFrame
from QueueClass import Queue
from PIL import Image, ImageTk
import numpy as np
import pickle
import matplotlib.pyplot as plt
import serial
import time
import os
import cv2
from datetime import date
from FLIRLib import BFSCam

import PySpin

class ControlHub:
    """Spawns a control hub for the laser system with various functionalities.
    Usage consists of instantiating a class and calling the .start() method

    """

    def __init__(self):
        self.window = tk.Tk(className='\Baldr Control Hub')
        self.screenwidth = str(int(self.window.winfo_screenwidth() * 0.35))
        self.screenheight = str(int(self.window.winfo_screenheight() * 0.35))
        self.window.geometry(self.screenwidth + 'x' + self.screenheight)
        self.grid = [16, 9]
        self.rowarr = list(i for i in range(self.grid[1]))
        self.colarr = list(i for i in range(self.grid[0]))
        self.window.rowconfigure(self.rowarr, minsize=25, weight=1)
        self.window.columnconfigure(self.colarr, minsize=25, weight=1)
        self.shotnum = 0
        self.shotfile = None
        self.imageframe = None
        self.imageframerunning = False
        self.laserArmed = False
        self.bfs = None
        self.queue = None
        self.temp_save_running = False
        self.filebrowser = None
        self.filename = None
        self.stage = None
        self.tempFile = None

        # migrate to class?
        self.system = PySpin.System.GetInstance()

        #self.bfs = BFSCam(self.system.GetCameras()[0])

        # title
        self.title_frame = tk.Frame(master=self.window, relief='raised', borderwidth=2)
        self.title_label = tk.Label(master=self.title_frame, text='Baldr Laser Control Hub Ver 0.0.1')
        self.title_frame.grid(row=0, column=0, columnspan=self.grid[0], sticky='new')
        self.title_label['font'] = font.Font(size=18)
        self.title_label.pack()

        # ################ LAUNCH FRAME ################
        self.launch_frame = tk.Frame(master=self.window, relief='groove', borderwidth=3)
        self.launch_frame.grid(row=1, column=0, rowspan=9, columnspan=3, sticky='nsew')
        self.stagelabel = tk.Label(master=self.launch_frame, text='Stage Control')
        self.stagelabel.grid(row=0, column=0, columnspan=3, sticky='ew' )
        # stage gui launch btn
        self.start_stage_btn = tk.Button(master=self.launch_frame, text='Launch Stage Control',
                                         command=self.__launchStageControl)
        self.start_stage_btn.grid(row=1, column=0, columnspan=3, sticky='nsew')

        # hdf5 storage file
        today = date.today()
        self.h5filepath = 'datafiles/'+today.strftime("%b-%d-%Y")

        if self.__createdir(self.h5filepath):
            print('dir made')
        self.__setShotFile()

        # Com port
        comlist = [comport.device for comport in serial.tools.list_ports.comports()]
        self.comval = tk.StringVar(self.launch_frame)
        # comval.set('Select Com Port')
        self.comval.set('COM4')
        self.comlabel = tk.Label(master=self.launch_frame, text='COM Port:')
        self.comlabel.grid(row=2, column=0, sticky='news')
        self.com = tk.OptionMenu(self.launch_frame, self.comval, *comlist)
        self.com.grid(row=2, column=1, sticky='nsew')

        # baud
        baudlist = [9600, 115200]
        self.baudval = tk.IntVar(self.launch_frame)
        self.baudval.set('115200')
        self.baudlabel = tk.Label(master=self.launch_frame, text='Baud Rate: ')
        self.baudlabel.grid(row=3, column=0, sticky='news')
        self.baud = tk.OptionMenu(self.launch_frame, self.baudval, *baudlist)
        self.baud.grid(row=3, column=1, sticky='nsew')
        # startup file
        self.filelabel = tk.Label(master=self.launch_frame, text='Startup File: ')
        self.filelabel.grid(row=4, column=0, sticky='news')
        self.startfile = tk.Entry(master=self.launch_frame)
        self.startfile.insert(0, 'Config/startup.txt')
        self.startfile.grid(row=4, column=1, sticky='nsew')

        self.h5header = tk.Label(master=self.launch_frame, text='HDF5 Files')
        self.h5header.grid(row=5, column=0, columnspan=3, sticky='ew')
        self.h5filetxt = tk.Label(master=self.launch_frame, text='File: '+str(self.shotfile))
        self.h5filetxt.grid(row=6, column=0, columnspan=3)

        # file browser gui button
        self.file_browser_btn = tk.Button(master=self.launch_frame, text='HDF5 File Browser',
                                          command=self.__launchHDFGUI)
        self.file_browser_btn.grid(row=7, column=0, columnspan=3, sticky='news')

        # program file input:
        self.programfiletext = tk.Label(master=self.launch_frame, text='Program File')
        self.programfileinput = tk.Entry(master=self.launch_frame)
        self.getprogramfilebutton = tk.Button(master=self.launch_frame, text='Get',
                                              command=lambda: self.__getRunFile(self.programfileinput.get()))
        self.runprogrambutton = tk.Button(master=self.launch_frame, text='Run')
        self.runprogrambutton['state'] = tk.DISABLED
        self.killButton = tk.Button(master=self.launch_frame, text='KILL', command=self.__killSwitch)

        self.programfiletext.grid(row=8, column=0, columnspan=3,  sticky='ew')
        self.programfileinput.grid(row=9, column=0, rowspan=1, columnspan=3, sticky='ew')
        self.getprogramfilebutton.grid(row=9, column=3, sticky='ew')
        self.runprogrambutton.grid(row=9, column=4, sticky='ew')


        # shoot the laser button
        self.lasertext = tk.Label(master=self.launch_frame, text='Laser Controls')
        self.lasertext.grid(row=10, column=0, columnspan=3, sticky='ew')
        self.armLaser_btn = tk.Button(master=self.launch_frame, text='Arm Laser', fg='#C02f1d',
                                        command=self.__armLaser)
        self.armLaser_btn.grid(column=0, columnspan=2, row=11, sticky='nsew')

        self.shootLaser_btn = tk.Button(master=self.launch_frame, text='Fire Laser', bg='#BEBEBE')
        self.shootLaser_btn.grid(column=0, columnspan=2, row=12, sticky='nsew')

        self.revive_button = tk.Button(master=self.launch_frame)



        # ################ READOUT FRAME ################
        self.readout_frame = tk.Frame(master=self.window, relief='groove', borderwidth=3)
        self.readout_frame.grid(row=1, column=4, rowspan=9, columnspan=9, sticky='nsew')
        self.readout_frame.rowconfigure(list(i for i in range(16)), weight=1)
        self.readout_frame.columnconfigure(list(i for i in range(9)), weight=1)

        self.get_spectra_btn = tk.Button(master=self.readout_frame, text='Get shot spectra',
                                         command=self.__captureimage)
        self.get_spectra_btn.grid(row=1, column=0, columnspan=3, sticky='new')

        self.stage_pos = tk.StringVar()
        self.stage_pos_lbl = tk.Label(master=self.readout_frame, textvariable=self.stage_pos)
        self.stage_pos_lbl.grid(row=0, column=0, columnspan=9, sticky='ew')
        self.stage_pos_lbl['font'] = font.Font(size=18)
        self.stage_pos.set('Stage Not Connected')

        self.camera1 = tk.StringVar()
        self.cam_lbl = tk.Label(master=self.readout_frame, textvariable=self.camera1)
        self.cam_lbl.grid(row=4, column=0, columnspan=9, sticky='ew')
        self.cam_lbl['font'] = font.Font(size=14)
        self.camera1.set('Camera Not Connected')


        self.window.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__setTempFile()

    def start(self):
        """
        Calls tkinter's mainloop function to start GUI

        :return: None
        """
        self.window.mainloop()

    def __on_closing(self):
        # if messagebox.askokcancel("Quit", "Quit? This will close all windows."):
            #self.window.destroy()
        if self.bfs:
            self.bfs.deInit()
        self.window.destroy()

    def __armLaser(self):
        if not self.laserArmed:
            self.armLaser_btn.config(bg='#228C22', fg='#FFFFFF')
            self.shootLaser_btn.config(command=self.__fireLaser, bg='#c02f1d', fg='#FFFFFF')
            self.laserArmed = True
        else:
            self.armLaser_btn.config(bg='#F0F0F0', fg='red')
            self.shootLaser_btn.config(command=tk.NONE, bg='#BEBEBE', fg='#000000')
            self.laserArmed = False

    def __fireLaser(self):
        """
        This will need to assert laser actually fired, send triggers to spectrometers and
        sensors, and record all data coming back. Since python is a single-threaded monster, I have been toying around
        with the idea of an external script that is fed data via a multithreaded pipe into a queue, where the data
        has both a target file and data to write. This way we can increase laser firing speed as we dont always have
        to wait for all data to write. Though, I'm not sure if this is necessary. Really, it's contingent on bandwidth
        data being collected.
        :return: None
        """
        self.__createShotFile()
        # fire

        # collect data

    def __launchStageControl(self):
        """
        Instantiates a TwoAxisStage control GUI for the two axis stage from it's respective class

        :return: None
        """
        try:
            self.stage = TwoAxisStage(self.comval.get(), self.baudval.get(), self.startfile.get())
            p = self.stage.getPos()
            self.stage_pos.set('X: %1.3f, Y: %1.3f' % (p[0], p[1]))
            self.window.after(50, self.__pollPosition)
        except Exception as e:
            print(e)
        else:
            return

    def __pollPosition(self):
        if self.stage.isOpen():
            p = self.stage.getPos()
            self.stage_pos.set('X: %1.3f, Y: %1.3f' % (p[0], p[1]))
            self.window.after(50, self.__pollPosition)
        else:
            self.stage_pos.set("Stage Not Connected")

    def __launchHDFGUI(self):
        """
        Instantiates a FileBrowser control GUI from it's respective class. Used to interact with HDF5 files easily.
        Error handling is totally hacked and should be re-thought

        :return: None
        """
        try:
            if self.filebrowser.state():
                return
        except AttributeError:
            pass
        except FileNotFoundError:
            self.filebrowser = None

        if not self.filebrowser:
            self.filebrowser = FileBrowser()

    def __createdir(self, name):
        try:
            os.makedirs(name)
        except OSError:
            return False
        else:
            return True

    def __setShotFile(self):
        owd = os.getcwd()
        try:
            os.chdir(self.h5filepath)
            dirs = os.listdir()
            if dirs == []:
                self.shotnum = 0
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
                        self.shotnum = int(lf1[i:])
                        break
            self.shotfile = 'shot' + '0' * (4 - len(str(self.shotnum))) + str(self.shotnum) + '.hdf5'
        except:
            print('something went wrong')
        finally:
            os.chdir(owd)

    def __createShotFile(self):
        owd = os.getcwd()
        try:
            os.chdir(self.h5filepath)
            self.shotnum += 1
            self.shotfile = 'shot' + '0' * (4 - len(str(self.shotnum))) + str(self.shotnum) + '.hdf5'
            h5m.createFile(self.shotfile)
            self.h5filetxt['text'] = 'File: ' + self.shotfile
        except Exception as e:
            print('Error occured creating shot file:' + e)

        finally:
            os.chdir(owd)

    def __captureimage(self):
        image = self.bfs.getImage()

        imgname = 'images/spectra_shot_00' + str(self.shotnum) + '.png'
        cv2.imwrite(imgname, image.GetNDArray())
        self.shotnum += 1
        print(self.imageframerunning)

        if not self.imageframerunning:
            self.imageframerunning = True
            self.imageframe = ImageFrame('Image', imgname)
        else:
            print('added')
            self.imageframe.addImage(imgname)

    def __getspectra(self):
        # this will get the plot of most recent shot spectra
        pass

    def __getRunFile(self, filename):
        try:
            assert os.path.exists(filename)
            self.filename = filename
            f = open(filename, 'r')
            self.queue = Queue()
            for line in f:
                if line != '' and line[0] != ';':
                    self.queue.enqueue(line)
            self.stage.sendOutput('\n' + '> ' + ' Loaded ' + filename)
        except:
            try:
                self.stage.sendOutput('\n' + '!> ' + ' File does not exist')
            except:
                self.programfileinput.delete(0, 'end')
                self.programfileinput.insert(0, 'Launch stage control first')
                self.window.after(1000, lambda: self.programfileinput.delete(0, 'end'))
            self.getprogramfilebutton.config(bg='red', command=tk.NONE)
            self.window.after(1000,
                              lambda: self.getprogramfilebutton.config(bg='#F0F0F0',
                                                                             command=lambda: self.__getRunFile(self.programfileinput.get())))
        else:
            self.__showKillButton()

    def __runProgram(self):
        if not self.temp_save_running:
            self.temp_save_running = True
            self.__saveTempData()

        next = self.queue.dequeue()
        self.__sendCommand(next)

        if self.queue.size() > 0:
            self.stage.sendCommand(next)
            self.window.after(50, self.__runProgram)
        #     self.window.after(self.calcDelay(self.currentpos, next), self.__runProgram)
        #     self.currentpos = next
        #
        elif self.queue.size() == 0:
            return
        #     self.window.after(self.calcDelay(self.currentpos, next), self.finishRun)
        #
        # else:
        #     self.temprunning = False
        #     return

    def __showKillButton(self):
        self.killButton.grid(row=9, column=5, sticky='ew')
        self.runprogrambutton['state'] = tk.ACTIVE
        self.runprogrambutton.config(command=self.__runProgram)

    def __sendCommand(self, command):
        print(command)

    def __killSwitch(self):
        if self.queue:
            self.queue.clear()
            self.temp_save_running = False
            self.stage.sendOutput('\n' + '!> ' + 'Current motion killed')

    def __setTempFile(self):
        """
        Sets the temporary file name, unless it exists

        :return: None
        """
        if os.path.exists('temp.npy') or self.tempFile is not None:
            print('temp exists')
            self.revive_button.grid(row=9, column=3, columnspan=2, sticky='nsew')
            self.revive_button.configure(text='Load\nData?', fg='red', command=self.__revive)
            self.__blinkButton(self.revive_button, 'red', 'blue', 1000)
        else:
            self.tempFile = 'temp.npy'

    def __saveTempData(self):
        """
        Saves temp data to temp file, if program is currently running it calls itself every 1000ms

        :return: None
        """
        if self.temp_save_running:
            if self.queue.size() > 0:
                np.save(self.tempFile, [self.queue.peek(), time.asctime(), self.filename, self.shotnum])
                self.window.after(1000, self.__saveTempData)
                return True
        else:
            return False

    def __retriveTempData(self):
        self.tempFile = 'temp.npy'
        currentline, t, self.filename, self.shotnum = np.load(self.tempFile, allow_pickle=True)
        print(currentline, t, self.filename)
        return currentline

    def __removeTempFile(self):
        """
        removes temp file at end of program run

        :return: None
        """
        os.remove(self.tempFile)
        self.tempFile = None

    def __revive(self):
        """
        Starts from an unexpected power loss. Retreives last known position from temp file.
        Issues: Target stage *could* be manually moved on us prior to reviving. User initiative to ensure
        nothing moves.

        :return: None
        """
        if self.stage:
            self.queue = None
            currentline = self.__retriveTempData()
            print(currentline)
            try:
                f = open(self.filename, 'r')
                self.queue = Queue()
                positionFound = False
                for line in f:
                    if line == currentline:
                        positionFound = True
                    if positionFound:
                        if line != '' and line[0] != ';':
                            self.queue.enqueue(line)
                self.stage.sendOutput('\n' + '> ' + ' Loaded ' + self.filename)
                self.revive_button.destroy()
                self.runprogrambutton['state'] = tk.ACTIVE
                self.runprogrambutton.config(command=self.__runProgram)
                self.__showKillButton()
            except FileNotFoundError:
                self.programfileinput.delete(0, 'end')
                self.programfileinput.insert(0, 'File does not exist')

        else:
            self.programfileinput.delete(0, 'end')
            self.programfileinput.insert(0, 'Launch stage control first')
            self.window.after(1000, lambda: self.programfileinput.delete(0, 'end'))

    def __blinkButton(self, button, c1, c2, delay):
        """
        Blinks a button between two colors, c1 and c2. Has logic for specific buttons to cease switching given a
        specific string as the text.

        :param button: target button instance
        :param c1: First color to switch to, string
        :param c2: Second color to switch to, string
        :param delay: Delay in ms
        :return: None
        """
        try:
            if button['text'] == 'Start?':
                return
            else:
                if button['fg'] == c1:
                    button.configure(fg=c2)
                else:
                    button.configure(fg=c1)
                self.window.after(delay, lambda: self.__blinkButton(button, c1, c2, delay))
        except:
            return