import tkinter as tk
from tkinter import ttk
import os
import numpy as np


class AddDiagnosticFrame:
    """
        Class to facilitate the addition and removal of diagnostic systems within the control hub.

        diagnosticfile format = {
            1: {
                param1: name
                param2: date
                param3: weather
            },
            2: {
                param1: name
                param2: date
                param3: weather
            },
            3: {
                param1: name
                param2: date
                param3: weather
            }, et cetera...
        }
    """
    diagnosticsFile = 'Config/DiagnosticConfig.npy'

    def __init__(self, master, num):
        self.master = master
        self.diag_num = num

        self.folders = ttk.Notebook(master=self.master)

        # # ########## FLIR
        # self.FLIRparams = {}
        # self.FLIRsubframe = tk.Frame(master=self.folders, relief='groove', borderwidth=2)
        # self.FLIRsubframe.rowconfigure(list(i for i in range(16)), minsize=1, weight=1)
        # self.FLIRsubframe.columnconfigure(list(i for i in range(16)), minsize=1, weight=1)
        # self.FLIRsubframe.grid(row=0, column=0, rowspan=9, columnspan=16, sticky='nsew')
        #
        # # list of availible diagnostics
        # self.dlist = [i+1 for i in range(num)]
        # self.FLIRselected_diagnostic = tk.IntVar()
        # self.FLIRselected_diagnostic.set(1)
        #
        # self.dropdown = tk.OptionMenu(self.FLIRsubframe, self.FLIRselected_diagnostic, *self.dlist)
        # self.dlabel = tk.Label(master=self.FLIRsubframe, text='Diagnostic Number:')
        # self.dlabel.grid(row=0, column=0, sticky='ew')
        # self.dropdown.grid(row=0, column=1, sticky='we')
        #
        # self.cameraname = tk.Label(master=self.FLIRsubframe, text='Name:')
        # self.cameraname.grid(row=1, column=0, sticky='ew')
        # self.cameranameentry = tk.Entry(master=self.FLIRsubframe)
        # self.cameranameentry.grid(row=1, column=1, sticky='ew')
        #
        # self.serialnumber = tk.Label(master=self.FLIRsubframe, text='Serial Number:')
        # self.serialnumber.grid(row=2, column=0, sticky='ew')
        # self.serialnumberentry = tk.Entry(master=self.FLIRsubframe)
        # self.serialnumberentry.grid(row=2, column=1, sticky='ew')
        #
        # self.flirfilepath = tk.Label(master=self.FLIRsubframe, text='Data File Path')
        # self.flirfilepath.grid(row=3, column=0, sticky='ew')
        # self.flirfilepathentry = tk.Entry(master=self.FLIRsubframe)
        # self.flirfilepathentry.grid(row=3, column=1, sticky='ew')
        #
        # self.FLIRstartenable = enableOnStartupButton(self.FLIRsubframe, 0, 4)
        #
        # self.addFlirButton = tk.Button(master=self.FLIRsubframe, text='Apply Changes',
        #                                command=self.__setFLIRParams)
        # self.addFlirButton.grid(row=5, column=0, columnspan=5)

        # name / intended  use?
        # data to expect?
        # location to store?

        # ########## General
        self.FLIRparams = {}
        self.FLIRsubframe = tk.Frame(master=self.folders, relief='groove', borderwidth=2)
        self.FLIRsubframe.rowconfigure(list(i for i in range(16)), minsize=1, weight=1)
        self.FLIRsubframe.columnconfigure(list(i for i in range(16)), minsize=1, weight=1)
        self.FLIRsubframe.grid(row=0, column=0, rowspan=9, columnspan=16, sticky='nsew')

        # list of availible diagnostics
        self.dlist = [i + 1 for i in range(num)]
        self.FLIRselected_diagnostic = tk.IntVar()
        self.FLIRselected_diagnostic.set(1)

        self.dropdown = tk.OptionMenu(self.FLIRsubframe, self.FLIRselected_diagnostic, *self.dlist)
        self.dlabel = tk.Label(master=self.FLIRsubframe, text='Diagnostic Number:')
        self.dlabel.grid(row=0, column=0, sticky='ew')
        self.dropdown.grid(row=0, column=1, sticky='we')

        self.cameraname = tk.Label(master=self.FLIRsubframe, text='Name:')
        self.cameraname.grid(row=1, column=0, sticky='ew')
        self.cameranameentry = tk.Entry(master=self.FLIRsubframe)
        self.cameranameentry.grid(row=1, column=1, sticky='ew')

        self.serialnumber = tk.Label(master=self.FLIRsubframe, text='Serial Number:')
        self.serialnumber.grid(row=2, column=0, sticky='ew')
        self.serialnumberentry = tk.Entry(master=self.FLIRsubframe)
        self.serialnumberentry.grid(row=2, column=1, sticky='ew')

        self.flirfilepath = tk.Label(master=self.FLIRsubframe, text='Data File Path')
        self.flirfilepath.grid(row=3, column=0, sticky='ew')
        self.flirfilepathentry = tk.Entry(master=self.FLIRsubframe)
        self.flirfilepathentry.grid(row=3, column=1, sticky='ew')

        self.datatypelabel = tk.Label(master=self.FLIRsubframe, text='Data Type:')
        self.datatypelabel.grid(row=4, column=0, sticky='ew')
        self.datatypevar = tk.StringVar()
        self.datatypelist = ['Image', 'Spectra', 'Interferometer', 'Other']
        self.datatypemenu = tk.OptionMenu(self.FLIRsubframe, self.datatypevar, *self.datatypelist)
        self.datatypemenu.grid(row=4, column=1, sticky='ew')

        self.FLIRstartenable = enableOnStartupButton(self.FLIRsubframe, 0, 5)

        self.addFlirButton = tk.Button(master=self.FLIRsubframe, text='Apply Changes',
                                       command=self.__setFLIRParams)
        self.addFlirButton.grid(row=6, column=0, columnspan=3, sticky='ew')

        # ######## STAGE
        self.Stagesubframe = tk.Frame(master=self.folders, relief='groove', borderwidth=2)
        self.Stagesubframe.rowconfigure(list(i for i in range(16)), minsize=1, weight=1)
        self.Stagesubframe.columnconfigure(list(i for i in range(16)), minsize=1, weight=1)
        self.Stagesubframe.grid(row=0, column=0, rowspan=9, columnspan=16, sticky='nsew')

        # yeah lol how am I gonna do this

        # ####### REMOVE
        self.remove_parameter_subframe = tk.Frame(master=self.folders)
        self.remove_parameter_subframe.rowconfigure(list(i for i in range(16)), minsize=1, weight=1)
        self.remove_parameter_subframe.columnconfigure(list(i for i in range(16)), minsize=1, weight=1)
        self.remove_parameter_subframe.grid(row=0, column=0, rowspan=9, columnspan=16, sticky='nsew')
        self.rmselected_diagnostic = tk.IntVar()
        self.rmdropdown = tk.OptionMenu(self.remove_parameter_subframe, self.rmselected_diagnostic, *self.dlist)
        self.rmdlabel = tk.Label(master=self.remove_parameter_subframe, text='Diagnostic Number:')
        self.rmdlabel.grid(row=0, column=0, sticky='ew')
        self.rmdropdown.grid(row=0, column=1, sticky='we')

        self.removeParameterButton = tk.Button(master=self.remove_parameter_subframe, text='Remove Parameter',
                                               command=lambda: self.__removeDiagnostic(
                                                   self.rmselected_diagnostic.get()))
        self.rmCheck2 = tk.Checkbutton(master=self.remove_parameter_subframe,
                                       text='I acknowledge that this diagnostic will cease to exist and '
                                            'need to be re-entered in the future',
                                       command=lambda: self.removeParameterButton.grid(row=3, column=0,
                                                                                       columnspan=5, sticky='we'))
        self.rmCheck1 = tk.Checkbutton(master=self.remove_parameter_subframe,
                                       text='I want to remove this diagnostic',
                                       command=lambda: self._toggleDiagnostic('show', self.rmCheck2, posy=2, posx=0))
        # lambda: self.rmCheck2.grid(row=2, column=0, columnspan=10, sticky='w')
        self.rmCheck1.grid(row=1, column=0, sticky='w')

        # ######## PACK
        self.folders.add(self.FLIRsubframe, text='General Diagnostic')
        self.folders.add(self.Stagesubframe, text='2 Axis Stage (LIBS ONLY)')
        self.folders.add(self.remove_parameter_subframe, text='Remove Parameters')
        self.folders.grid(row=0, column=0, rowspan=9, columnspan=16, sticky='nsew')

    def __setFLIRParams(self):
        # todo: set new params in diag file
        #       implement new methods to determine if we can pull image data from whatever and stuff
        # check if diagnostics file exists
        if os.path.exists(self.diagnosticsFile):
            diagnostics = np.load(self.diagnosticsFile, allow_pickle='True')
            if len(diagnostics.item().keys()) != 0 and self.FLIRselected_diagnostic.get() in diagnostics.item().keys():
                # todo: handle overwrite prompt
                self.addFlirButton.config(text='Diagnostic already exists')
                self.master.after(2000, lambda: self.addFlirButton.config(text='Apply Changes'))
                return
        else:
            # if it doesnt exits, create and save an empty dictionary to it
            tempdict = {}
            np.save(self.diagnosticsFile, tempdict)
        # TODO: parse for correctness, not just emptiness. PathExists, etc
        #   Also, *type* of data (image, pos, spectra, etc)
        # ensure all boxes have input in them - doesnt check correctness
        if self.cameranameentry.get().strip() == '':
            self.cameraname.config(text='Enter Camera Name', fg='red')
            self.master.after(3000, lambda: self.cameraname.config(text='Name:', fg='black'))
            return
        if self.serialnumberentry.get().strip() == '':
            self.serialnumber.config(text='Enter Serial Number', fg='red')
            self.master.after(3000, lambda: self.serialnumber.config(text='Serial Number:', fg='black'))
            return
        if self.serialnumberentry.get().strip() == '':
            self.serialnumber.config(text='Enter Serial Number', fg='red')
            self.master.after(3000, lambda: self.serialnumber.config(text='Name:', fg='black'))
            return
        if not os.path.exists(self.flirfilepathentry.get().strip()):
            self.flirfilepath.config(text='Must be valid directory', fg='red')
            self.master.after(3000, lambda: self.flirfilepath.config(text='Data File Path:', fg='black'))

        # add pairs to dictionary from input boxes
        self.FLIRparams['Diagnostic Name'] = self.cameranameentry.get()
        self.FLIRparams['Serial Number'] = self.serialnumberentry.get()
        self.FLIRparams['DataType'] = self.datatypevar.get()
        self.FLIRparams['File Path'] = self.flirfilepathentry.get()
        self.FLIRparams['Enabled On Startup'] = self.FLIRstartenable.isEnabled()

        # save to diagnostics file
        diagdict = np.load(self.diagnosticsFile, allow_pickle='True').item()
        diagdict[int(self.FLIRselected_diagnostic.get())] = self.FLIRparams
        np.save(self.diagnosticsFile, diagdict)
        self.addFlirButton.config(text='Diagnostic saved!')
        self.master.after(2000, lambda: self.addFlirButton.config(text='Apply Changes'))
        return

    def __removeDiagnostic(self, num):
        # remove specific diag from file
        try:
            d = np.load(self.diagnosticsFile, allow_pickle=True).item()
            d.pop(num)
            np.save(self.diagnosticsFile, d)
            self.removeParameterButton.grid_remove()
            self.rmCheck2.grid_remove()
            self.rmCheck1.setvar(tk.FALSE)
        except:
            pass


    def _toggleDiagnostic(self, opt, target, posx=None, posy=None):
        try:
            if opt == 'show':
                target.grid()
        except:
            pass


class enableOnStartupButton:
    # todo: Check if enabled and then activate within controlhub
    def __init__(self, master, posx, posy):
        self.enabled = tk.IntVar()
        self.enabledButton = tk.Checkbutton(master=master, text='Enable on startup: ', variable=self.enabled)
        self.enabledButton.grid(row=posy, column=posx, columnspan=2)

    def isEnabled(self):
        return bool(self.enabled.get())
