import warnings; warnings.filterwarnings('ignore')
import tkinter as tk
from tkinter import ttk
from tkinter import font, messagebox
from droogCNC import TwoAxisStage
from HDF5Browser import FileBrowser
import HDF5Methods as h5m
import serial.tools.list_ports
from ImageViewer import ImageFrame
from QueueClass import Queue
from DiagnosticAddingClass import AddDiagnosticFrame
import numpy as np
import serial
import time
import os
from datetime import date
import PySpin
import DataParsing
import WriteDataToHDF5
os.system('cls')

class ControlHub:
    """Spawns a control hub for the laser system with various functionalities.
    Usage consists of instantiating a class and calling the .start() method

    """

    def __init__(self):
        self.window = tk.Tk(className='\Baldr Control Hub')
        self.screenwidth = int(self.window.winfo_screenwidth() * 0.55)
        self.screenheight = int(self.window.winfo_screenheight() * 0.55)
        self.grid = [16, 9]
        self.rowarr = list(i for i in range(self.grid[1]))
        self.colarr = list(i for i in range(self.grid[0]))
        self.window.rowconfigure(self.rowarr, minsize=25, weight=1)
        self.window.columnconfigure(self.colarr, minsize=25, weight=1)

        self.tabcontrol = ttk.Notebook(self.window)

        self.diagnosticsFile = AddDiagnosticFrame.diagnosticsFile
        self.control_tab = ttk.Frame(self.tabcontrol)
        self.diag_tab = ttk.Frame(self.tabcontrol)
        self.diag_config = ttk.Frame(self.tabcontrol)

        self.control_tab.rowconfigure(self.rowarr, minsize=25, weight=1)
        self.control_tab.columnconfigure(self.colarr, minsize=25, weight=1)

        self.diag_row_arr = list(i for i in range(3))
        self.diag_tab.rowconfigure(self.diag_row_arr, minsize=1, weight=1)
        self.diag_tab.columnconfigure(self.diag_row_arr, minsize=1, weight=1)

        self.control_tab_name = 'Control'
        self.diag_tab_name = 'Configure Diagnostics'
        self.diag_config_name = 'Add / Remove Diagnostics'
        self.tabcontrol.add(self.control_tab, text=self.control_tab_name)
        self.tabcontrol.add(self.diag_tab, text=self.diag_tab_name)
        self.tabcontrol.add(self.diag_config, text=self.diag_config_name)
        self.tabcontrol.grid(row=1, column=0, rowspan=self.grid[1] - 1, columnspan=self.grid[0], sticky='news')

        # refresh page whenever tab is clicked:
        self.tabcontrol.bind("<<NotebookTabChanged>>", self.__handle_tab_change)

        self.diag_config.rowconfigure([1], minsize=25, weight=1)
        self.diag_config.columnconfigure([1], minsize=25, weight=1)
        self.Diagnostics_list = []

        for i in range(len(self.diag_row_arr)):
            for j in range(len(self.diag_row_arr)):
                self.Diagnostics_list.append(DiagnosticFrame(self.diag_tab, i, j))

        self.diagnosticEditor = AddDiagnosticFrame(self.diag_config, len(self.Diagnostics_list))
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
        self.stageparameters = {}
        # migrate to class?
        self.system = PySpin.System.GetInstance()

        # self.bfs = BFSTrigger()
        self.bfs = None

        # title
        self.title_frame = tk.Frame(master=self.window, relief='raised', borderwidth=2)
        self.title_label = tk.Label(master=self.title_frame, text='Baldr Laser Control Hub Ver 0.0.1')
        self.title_frame.grid(row=0, column=0, columnspan=self.grid[0], sticky='new')
        self.title_label['font'] = font.Font(size=18)
        self.title_label.pack()

        # ################ LAUNCH FRAME ################
        self.launch_frame = tk.Frame(master=self.control_tab, relief='groove', borderwidth=3)
        self.launch_frame.grid(row=1, column=0, rowspan=9, columnspan=3, sticky='nsew')
        self.stagelabel = tk.Label(master=self.launch_frame, text='Stage Control')
        self.stagelabel.grid(row=0, column=0, columnspan=3, sticky='ew')
        # stage gui launch btn
        self.start_stage_btn = tk.Button(master=self.launch_frame, text='Launch Stage Control',
                                         command=self.__launchStageControl)
        self.start_stage_btn.grid(row=1, column=0, columnspan=3, sticky='nsew')

        # hdf5 storage file
        today = date.today()
        self.h5filepath = 'DataFiles/' + today.strftime("%b-%d-%Y")
        self.tempdatapath = 'DataFiles/queue/'
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
        self.h5filetxt = tk.Label(master=self.launch_frame, text='File: ' + str(self.shotfile))
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

        self.programfiletext.grid(row=8, column=0, columnspan=3, sticky='ew')
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
        self.shootLaser_btn['state'] = tk.DISABLED

        self.revive_button = tk.Button(master=self.launch_frame)

        # ################ READOUT FRAME ################
        self.readout_frame = tk.Frame(master=self.control_tab, relief='groove', borderwidth=3)
        self.readout_frame.grid(row=1, column=4, rowspan=9, columnspan=9, sticky='nsew')
        self.readout_frame.rowconfigure(list(i for i in range(16)), weight=1)
        self.readout_frame.columnconfigure(list(i for i in range(9)), weight=1)

        self.get_spectra_btn = tk.Button(master=self.readout_frame, text='Get last image',
                                         command=self.__getCurrentImage)
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

        if self.bfs:
            self.camera1.set('Camera Connected')

        self.window.geometry(
            '%dx%d+%d+%d' % (self.screenwidth, self.screenheight, self.window.winfo_screenwidth() / 4,
                             self.window.winfo_screenheight() / 5))
        self.window.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__setTempFile()
        self.window.update()
        # now root.geometry() returns valid size/placement
        self.window.minsize(self.window.winfo_width(), self.window.winfo_height())

        # create data watch instance
        self.watchDogList = []
        self.__startH5Watchdog()
        self.__startFileWatchdogs()

    def start(self):
        """
        Calls tkinter's mainloop function to start GUI

        :return: None
        """
        self.window.mainloop()

    def __on_closing(self):
        # if messagebox.askokcancel("Quit", "Quit? This will close all windows."):
        # self.window.destroy()
        for i in self.watchDogList:
            i.kill()
        self.h5writer.kill()
        self.window.destroy()

    def __armLaser(self):
        # if self.stage != None:
        #     if not self.laserArmed:
        #         self.shootLaser_btn['state'] = tk.ACTIVE
        #         self.armLaser_btn.config(bg='#228C22', fg='#FFFFFF')
        #         self.shootLaser_btn.config(command=self.__fireLaser, bg='#c02f1d', fg='#FFFFFF')
        #         self.laserArmed = True
        #         self.bfs.init()
        #     else:
        #         self.armLaser_btn.config(bg='#F0F0F0', fg='red')
        #         self.shootLaser_btn['state'] = tk.DISABLED
        #         self.shootLaser_btn.config(command=tk.NONE, bg='#BEBEBE', fg='#000000')
        #         self.laserArmed = False
        #         self.bfs.deinit()

            self.shootLaser_btn['state'] = tk.ACTIVE
            self.armLaser_btn.config(bg='#228C22', fg='#FFFFFF')
            self.shootLaser_btn.config(command=self.__fireLaser, bg='#c02f1d', fg='#FFFFFF')
            self.laserArmed = True

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
        # if self.stage.isOpen():
        self.__createShotFile()
            # image = self.__captureimage()
            # # self.__triggerLaser()
            # # self.__takePicture() for all cameras?? Multithreaded might be needed here for simultaneity
            # self.__saveData(image)

    def __saveData(self, image):
        # stage:
        st = time.time()
        owd = os.getcwd()
        try:
            os.chdir(self.h5filepath)
            h5m.createDataset(self.shotfile, 'StagePos', data=self.stage.getPos())
            for key, val in self.stage.getStageParameters().items():
                h5m.setMetadata(self.shotfile, str(key), str(val), path='StagePos')
            h5m.createDataset(self.shotfile, 'BFSimage', data=image)
            h5m.setMetadataFromDict(self.shotfile, self.bfs.getDeviceParams(), path='BFSimage')
        except Exception as e:
            print('Error occured saving data')
            print(e)
        finally:
            os.chdir(owd)
            print('saving data took ' + str(time.time() - st) + ' seconds')

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
            self.filebrowser.parseCommand('cd ' + self.h5filepath)

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
            # dirs = [file for file in os.listdir()
            #         if os.path.isfile(os.path.join(self.h5filepath+'\\', file))]
            dirs = [file for file in os.listdir()
                    if os.path.isfile(file)]
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
        except Exception as e:
            print('something went wrong', e)
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
            print('Error occured creating shot file:', e)

        finally:
            os.chdir(owd)

    def __captureimage(self):
        return self.bfs.run_single_camera(self.bfs.cam)

    def __getCurrentImage(self):
        owd = os.getcwd()
        try:
            os.chdir(self.h5filepath)
            image = h5m.getData(self.shotfile, 'BFSimage')
            self.imageframe = ImageFrame('', image=image)
        except Exception as e:
            print(e)
        finally:
            os.chdir(owd)

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
                                                                       command=lambda: self.__getRunFile(
                                                                           self.programfileinput.get())))
        else:
            self.__showKillButton()

    def __runProgram(self):
        if not self.temp_save_running:
            self.temp_save_running = True
            self.__saveTempData()
        if not self.queue.is_empty():
            next = self.queue.dequeue()
            self.__sendCommand(next)
        else:
            self.stage.sendOutput('Run Finished')
            self.__finishRun()

    def __showKillButton(self):
        self.killButton.grid(row=9, column=5, sticky='ew')
        self.runprogrambutton['state'] = tk.ACTIVE
        self.runprogrambutton.config(command=self.__runProgram)

    def __sendCommand(self, command):
        if command.strip().lower() != 'fire':
            if self.queue.size() >= 0:
                self.stage.sendCommand(command)
                self.window.after(1000, self.__runProgram)
            #     self.window.after(self.calcDelay(self.currentpos, next), self.__runProgram)
            #     self.currentpos = next
            #
            # elif self.queue.size() == 0:
            #     self.__finishRun()
            # else:
            #     self.temp_save_running = False
            #     return
        else:
            self.__fireLaser()
            self.window.after(1000, self.__runProgram)

    def __finishRun(self):
        """
        removes temp file at end of program run

        :return: None
        """
        print('finish run called')
        os.remove(self.tempFile)
        self.tempFile = None

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
        # todo: implement different method for finding lost position - right now if there
                are duplicates it will break ://
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

    def __calculateStageDelay_ms(self, currentpos, nextpos):
        ipos = self.__parsePosition(currentpos)
        fpos = self.__parsePosition(nextpos)
        assert len(ipos) == len(fpos), 'Input arrays must be same length'

        v = float(self.stage.getStageParameters()['xMaxRate'][1]) / 60
        a = float(self.stage.getStageParameters()['xMaxRate'][1])  # becomes very choppy changing to xMaxAcc... idk wtf

        delta = list(ipos[i] - fpos[i] for i in range(len(ipos)))
        d = np.sqrt(sum(i ** 2 for i in delta))
        deltaT = ((2 * v) / a) + ((d - (v ** 2 / a)) / v)
        print('next move in ' + str(int(np.floor(deltaT * 1000))) + 'ms')
        return int(np.floor(deltaT * 1000))  # in ms

    def __parsePosition(self, ipos):
        """
        Parses position for use with DRO

        :param ipos: input position
        :return: [x, y] list of current position
        """
        pos = [0, 0]
        for i in ipos.split(' '):
            if i.lower()[0] == 'x':
                pos[0] = float(i[1:])
            if i.lower()[0] == 'y':
                pos[1] = float(i[1:])
        return pos

    def __handle_tab_change(self, event):
        if self.tabcontrol.tab(self.tabcontrol.select())['text'] == self.diag_tab_name:
            self.__refreshDiagnosticsTab()

    def __refreshDiagnosticsTab(self):
        if os.path.exists(self.diagnosticsFile):
            d = np.load(self.diagnosticsFile, allow_pickle=True).item()
            for i in d.keys():
                target = self.Diagnostics_list[i - 1]
                target.clearText()
                for key, val in d[i].items():
                    if key == 'Diagnostic Name':
                        target.name_entry.config(text=val)
                    elif key == 'File Path':
                        target.dir_entry.config(text=val)
                    elif key == 'Enabled On Startup':
                        target.enabled.set(1)

    def __startFileWatchdogs(self):
        if os.path.exists(self.diagnosticsFile):
            d = np.load(self.diagnosticsFile, allow_pickle=True).item()
            for i in d.keys():
                self.watchDogList.append(DataParsing.DataDaemon(d[i]['File Path'] + '/', self.tempdatapath, 5))
        for i in self.watchDogList:
            i.main()

    def __startH5Watchdog(self):
        self.h5writer = WriteDataToHDF5.HDF5Writer(self.tempdatapath, self.h5filepath)
        self.h5writer.start()

class DiagnosticFrame:
    def __init__(self, master, posx, posy):
        self.master = master
        self.xpos = posx
        self.ypos = posy
        self.subframe = tk.Frame(master=self.master, relief='raised', borderwidth=2)
        self.subframe.rowconfigure(list(i for i in range(4)), minsize=1, weight=1)
        self.subframe.columnconfigure(list(i for i in range(2)), minsize=1, weight=1)
        self.subframe.grid(row=self.xpos, column=self.ypos, sticky='nsew')

        self.name = tk.Label(master=self.subframe, text='Diagnostic Name')
        self.name.grid(row=0, column=0)
        self.name_entry = tk.Label(master=self.subframe, relief='groove')
        self.name_entry.grid(row=0, column=1, sticky='ew')

        self.dir_label = tk.Label(master=self.subframe, text='Directory')
        self.dir_label.grid(row=1, column=0)
        self.dir_entry = tk.Label(master=self.subframe, relief='groove')
        self.dir_entry.grid(row=1, column=1, sticky='ew')

        self.enabled = tk.IntVar()
        self.enabledButton = tk.Checkbutton(master=self.subframe, text='Enable Diagnostic', variable=self.enabled)
        self.enabledButton.grid(row=2, column=0, columnspan=2)

    def clearText(self):
        self.name_entry.config(text='')
        self.dir_entry.config(text='')
        self.enabled.set(0)


if __name__ == '__main__':
    console = ControlHub()
    console.start()
