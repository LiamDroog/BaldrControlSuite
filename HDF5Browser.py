import h5py
import HDF5Methods as h5m
import os
import tkinter as tk
import time
from ImageViewer import ImageFrame


class FileBrowser:
    """
    This provides a user-friendly interface to deal with HDF5 files. Instantiate by assigning to a variable and calling
    .start()
    """

    # todo:
    #   Get file -done
    #   Create file -done (assertions?)
    #   rm File - opting for not right now
    #   create / edit metadata - done ( edge cases?)
    #   Create datasets
    #   Rename groups/sets?
    #   cd methods - done
    #   add visual cues for all
    #   export to csv or xlsx
    def __init__(self, subprocess=True):
        if subprocess:
            self.window = tk.Toplevel()
        else:
            self.window = tk.Tk(className='\HDF5 File Viewer')

        self.window.title('HDF5 File Viewer')
        self.screenwidth = str(int(self.window.winfo_screenwidth() * 0.35))
        self.screenheight = str(int(self.window.winfo_screenheight() * 0.35))
        self.window.geometry(self.screenwidth + 'x' + self.screenheight)
        self.grid = [16, 9]
        self.rowarr = list(i for i in range(self.grid[1]))
        self.colarr = list(i for i in range(self.grid[0]))
        self.window.rowconfigure(self.rowarr, minsize=25, weight=1)
        self.window.columnconfigure(self.colarr, minsize=25, weight=1)
        self.currentfile = None
        self.currentpath = '/'
        self.currentgroup = None
        self.currentdataset = None
        self.wraplength = 75
        self.outpadlen = 6
        self.anchorPos = [0, 5]
        self.help_dict = {}
        self.owd = os.getcwd()
        self.errmessage = 'Command not found. Try $help'

        self.entrybar = tk.Entry(master=self.window)
        self.entrybar.configure(width=40)
        self.entrybar.grid(row=self.grid[1], column=0, columnspan=6, sticky='new')

        self.sendentrybtn = tk.Button(master=self.window, text='Send',
                                      command=lambda: self.parseCommand(self.entrybar.get()))
        self.sendentrybtn.grid(row=self.grid[1], column=7, sticky='ew')

        self.output = tk.Listbox(master=self.window)
        self.output.grid(columnspan=8, rowspan=self.grid[1], row=0, column=0, sticky='nesw')
        self.output.configure(bg='white')
        self.window.bind('<Return>', (lambda x: self.parseCommand(self.entrybar.get())))

        self.scrollbar = tk.Scrollbar(master=self.window)
        self.scrollbar.grid(column=8, row=0, rowspan=self.grid[1], sticky='nsw')
        self.output.config(yscrollcommand=self.scrollbar.set)

        self.cwd_label = tk.Label(master=self.window,
                                  text='Working Directory: ~/> /' + '/'.join(i for i in os.getcwd().split('\\')[-3:]))
        self.cwd_label.grid(row=self.anchorPos[0], column=self.anchorPos[1] + 4, columnspan=10, sticky='w')

        self.currentfile_label = tk.Label(master=self.window, text='Current file: ')
        self.currentfile_label.grid(row=self.anchorPos[0] + 1, column=self.anchorPos[1] + 5, columnspan=10, sticky='w')

        # self.currentfilemethods = tk.Frame(master=self.window, bg='grey')
        # self.currentfilemethods.grid(row=self.anchorPos[0] + 2, column=self.anchorPos[1] + 4,
        #                              columnspan=6, rowspan=6, sticky='nsew')
        # self.tree_btn = tk.Button(master=self.currentfilemethods, text='Tree',
        #                           command=lambda: self.__tree(self.currentfile))
        # self.tree_btn.pack()
        self.__parseHelp()

        self.headstr = ['       __  __    ______ _           __    ____    ______  _             __',
                        '      / / / /   / ____/  | |       / /   /  _/   / ____/  | |           / /',
                        '    / /_/  /  /___ \     | |     / /    / /    / __/        | |   /|    / / ',
                        '  / __  /   ____/ /      | |  / /   _/ /    / /___         | |  / |  / /  ',
                        '/_/ /_/  /_____/       |___/   /___/  /_____/        |__/|__/   ']
        for i in self.headstr:
            self.__sendOutput(i, head=' ' * 8)
        self.__sendOutput(time.asctime(), head='>> ')
        self.__sendOutput('Written by Liam Droog', head='>> ')
        self.__sendOutput("HDF5 Methods Initialized", head='>> ')
        self.window.protocol("WM_DELETE_WINDOW", self.__onClose)
        self.window.geometry('800x400+%d+%d' % (self.window.winfo_screenwidth() / 4 + 810,
                                                self.window.winfo_screenheight() / 5 + 440))

    def start(self):
        """
        Starts GUI loop

        :return: None
        """
        self.window.mainloop()

    def state(self):
        try:
            r = self.window.state()
        except:
            raise FileNotFoundError
        else:
            return r

    def __getImage(self, dataset):
        try:
            image = h5m.getData(self.currentfile, dataset)
            ImageFrame('', image=image)
        except:
            self.__sendOutput('File does not have an image')

    def __getDirImages(self):
        dirs = os.listdir()
        if dirs == []:
            self.__sendOutput('No images found')
            return
        else:
            for i in range(len(dirs)):
                if dirs[i][-5:] != '.hdf5':
                    dirs.pop(i)
        if dirs == []:
            self.__sendOutput('No images found')
            return
        imageviewer = None
        for i in range(len(dirs)):
            try:
                image = h5m.getData(dirs[i], 'BFSimage')
                imageviewer = ImageFrame('', image=image)
            except:
                pass
            else:
                break

        if not imageviewer:
            self.__sendOutput('No pictures found')
            return

        for j in range(i, len(dirs)):
            imageviewer.addImage(h5m.getData(dirs[i], 'BFSimage'))
        print(imageviewer.getsize())

    def __onClose(self):
        os.chdir(self.owd)
        self.window.destroy()

    def parseCommand(self, command):
        """
        Parses command typed from input location. Resets text in input box after completion.

        :param command: Command to parse, string
        :return: None
        """
        # parses commands from input box (typed). resets input box to nil
        if command.strip() == '':
            return
        self.__sendCommand(command)
        if command[0] != '$':
            try:
                if command.strip() != '':
                    i = command.lower().strip().split(' ')
                    if i[0] == 'cls':
                        self.__cls()
                    elif i[0] == 'ls':
                        self.__ls()
                    elif i[0] == 'cd':
                        self.__cd(i[1])
            except Exception as e:
                print(e)

            finally:
                self.entrybar.delete(0, 'end')
                return
        else:
            try:
                parsedcommand = command.split('$')
                i = parsedcommand[1]
            except:
                self.__errmessage()
                return
            else:
                if i.strip() != '':
                    i = i.strip().split(' ')
                    if i[0] == 'get':
                        self.__getFile(i[1])
                    elif i[0] == 'create':
                        self.__createFile(i[1])
                    elif i[0] == 'setmetadata':
                        self.__setMetadata(' '.join(j for j in i[1:]))
                    elif i[0] == 'getmetadata':
                        if len(i) == 1:
                            if self.currentfile is None:
                                self.__sendOutput('No file selected')
                                return
                            self.__getMetadata(self.currentfile)
                        else:
                            self.currentfile = i[1]
                            self.__getMetadata(i[1])
                    elif i[0] == 'tree':
                        if len(i) == 1:
                            if self.currentfile is None:
                                self.__sendOutput('No file selected')
                                return
                            self.__tree(self.currentfile)
                        else:
                            self.__tree(i[1])
                    elif i[0] == 'help':
                        if len(i) == 1:
                            self.__help()
                        else:
                            self.__help(i[1].strip())
                    elif i[0] == 'getimage':
                        # TODO: Add to diagnostic config entry saying datatype is an image
                        #       so that we can filter here for display or not
                        self.__getImage(' '.join(j for j in i[1:]))
                    elif i[0] == 'getdirimages':
                        self.__getDirImages()
                    else:
                        self.__errmessage()

            self.entrybar.delete(0, 'end')

    def __sendCommand(self, command):
        """
        Displays sent command into the output box from the bottom to the top, scrolls to match most recent entry

        :param command: Command to display, string
        :return: None
        """
        # executes command based off input command
        self.output.insert('end', '\n' + '~> ' + command.rstrip()[0:self.wraplength])
        for i in range(self.wraplength, len(command.rstrip()), self.wraplength):
            self.output.insert('end', '\n' + '           ' + command.rstrip()[i:i + self.wraplength])
        self.output.yview(tk.END)

    def __sendOutput(self, command, head='!>'):
        """
        Displays output from sent command in output box

        :param command: Command to display, string
        :param head: leading character (!> for error, >> for generic, etc.)
        :return:
        """
        self.output.insert('end', '\n' + head + command.rstrip()[0:self.wraplength])
        for i in range(self.wraplength, len(command.rstrip()), self.wraplength):
            self.output.insert('end', '\n' + '           ' + command.rstrip()[i:i + self.wraplength])
        self.output.yview(tk.END)

    def __cls(self):
        """
        Like Linux command. Clears output box.

        :return: None
        """
        self.output.delete(0, tk.END)
        for i in self.headstr:
            self.__sendOutput(i, head=' ' * 8)
        self.__sendOutput('Written by Liam Droog', head='>> ')

    def __ls(self):
        """
        Like Linux command. Lists all files and subdirectories within current directory. Utilizes Python's os methods

        :return: None
        """
        self.__sendOutput(os.getcwd(), head='CWD: ')
        for i in os.listdir():
            if os.path.isdir(i):
                self.__sendOutput(i, head=' ' * 9 + '\u21B3')
            else:
                self.__sendOutput(i, head=' ' * 9 + '\u2192')

    def __cd(self, dir):
        """
        Like Linux command. Changes current directry via python's os methods.

        :param dir:
        :return:
        """
        if not os.path.isdir(dir):
            self.__sendOutput('Directory does not exist. Yet. ', head=' ' * self.outpadlen)
        else:
            os.chdir(dir)
            self.cwd_label.config(text='Working Directory: ~/> /' + '/'.join(i for i in os.getcwd().split('\\')[-3:]))
            self.currentfile = None
            self.currentfile_label.config(text='Current File: ')

    def __help(self, input=None):
        """
        Syntax: $help command
        This displays help for a given command or all if none are specified

        :param input: string to parse for command
        :return: None
        """
        if not input:
            for key, val in self.help_dict.items():
                self.__sendOutput('$' + key + ' Usage: ' + val, head='HELP: ')
            return
        if input not in self.help_dict.keys():
            self.__sendOutput("Unknown command")
            return
        if input:
            self.__sendOutput('$' + input + ' Usage: ' + self.help_dict[input], head='HELP: ')

    def __parseHelp(self, file='Config/H5Help.txt', delim=';;'):
        """
        Parses commands and their respective help outputs from input text file

        :param file: Target file
        :param delim: Delimiter to split at
        :return: None
        """
        try:
            with open(file, 'r') as f:
                for i in f:
                    j = i.rstrip().split(delim)
                    self.help_dict[j[0]] = j[1]
        except FileNotFoundError:
            print('Searching aimlessly for a file that does not exist.')
            self.__sendOutput('Searching aimlessly for a file that does not exist.')
        except Exception as e:
            print('Something has gone horribly wrong - ' + str(e))
            self.__sendOutput('Something has gone horribly wrong - ' + str(e))

    def __errmessage(self):
        """
        Displays an error message if something has gone terribly wrong.

        :return:  A bug that needs fixing, likely.
        """
        self.__sendOutput(self.errmessage)

    def __getFile(self, filename):
        """
        Gets input file if it exists such that operations can be performed on it. Gets all philosophical if a file
        isn't found, so I'd recommend making sure your files exits before calling method.

        :param filename: filename or path to target file, string
        :return: None
        """
        if filename.split('.')[-1].lower() not in ['hdf5', 'h5', 'he5']:
            self.__sendOutput('Invalid file format, must have extension [.hdf5, .h5, .he5]', head=' ' * self.outpadlen)
            return

        if os.path.exists(filename):
            self.currentfile = filename
            self.currentfile_label.config(text='Current File: ' + filename)
            self.__sendOutput('Got ' + filename, head=' ' * self.outpadlen)
        else:
            self.__sendOutput('File does not exist. What does it mean to exist, anyway?')

    def __createFile(self, filename):
        """
        Creates HDF5 file in current directory with given input filename.
        Swears like an old chap if unable to create file.

        :param filename: Name of file to be created, string
        :return: None
        """
        if filename.split('.')[-1].lower() not in ['.hdf5', '.h5', '.he5']:
            self.__sendOutput('Invalid file format, must have extension [.hdf5, .h5, .he5]', head=' ' * self.outpadlen)
            return

        if h5m.createFile(filename):
            self.__sendOutput('File successfully created', head=' ' * self.outpadlen)
            self.__getFile(filename)
            return
        else:
            self.__sendOutput('Unable to create file. Horsefeathers.', head=' ' * self.outpadlen)
            return

    def __createGroup(self):
        """
        Will create a group within a specified hdf5 file. yet to be implemented.

        :return: None
        """
        pass

    def __getMetadata(self, filename):
        """
        Gets parent file metadata from a given hdf5 file and outputs it to the output box.

        :param filename: target filename, string
        :return: None
        """
        if self.currentfile:
            self.__sendOutput('/' + filename, head='')
            self.__sendOutput('File Metadata:')
            for key, val in h5m.getMetadata(filename):
                self.__sendOutput(' ' * 5 + "%s: %s" % (key, val), head='')
        else:
            self.__sendOutput('Metadata failed to appear. Fiddlesticks.')

    def __setMetadata(self, iput, path='/'):
        """
        Sets metadata for a given file or dataset, specified by path

        :param iput: Input string of metadata separated by a comma - ie, 'this is a key, this is a value'
        :param path: path of dataset within HDF5 file, '/' refers to the parent file
        :return: None
        """
        cmd = iput.split(',')
        print(cmd)
        if len(cmd) < 2:
            self.__sendOutput('Too few arguments, '
                              '$setmetadata must have an attribute and a corresponding value separated by commas')
        else:
            h5m.setMetadata(self.currentfile, cmd[0], cmd[1], path=path)

    def __tree(self, filename):
        """
        Similar to windows style tree command, displays all groups and datasets for a given hdf5 file

        :param filename: target filename, string
        :return: None
        """
        try:
            if os.path.exists(filename):
                with h5py.File(filename, mode='a') as h5f:
                    self.__getMetadata(filename)
                    h5f.visititems(self.__print_attrs)
            else:
                self.__sendOutput('File does not exist')
        except:
            print('error with tree')
            self.__sendOutput('Error generating tree - Have you selected a file?')
    def __outputTree(self, filename):
        """
        Not operational. Not sure if this is needed in the end product

        :param filename: target filname
        :return: None
        """
        if os.path.exists(filename):
            with h5py.File(filename, mode='a') as h5f:
                self.__getMetadata(filename)
                h5f.visititems(self.__print_attrs)
        else:
            self.__sendOutput('File does not exist')

    def __rmFile(self):
        """
        Not operational. Not sure if I would include this in final product

        :return: Woe and misery if used incorrectly
        """
        pass

    def __print_attrs(self, name, obj):
        """
        Used for H5py's visititems method to get all group and dataset metadata in one fell swoop

        :param name: Group in question
        :param obj: Dataset in question
        :return: None
        """
        try:
            self.__sendOutput('/' + name, head='')
            n = 9
            self.__sendOutput('    Shape: ' + str(obj.shape), head=' ')
            self.__sendOutput('    Type: ' + str(obj.dtype), head=' ')
            self.__sendOutput('    Compression: ' + str(obj.compression), head=' ')
            self.__sendOutput(' ' * n + 'Metadata:', head='')
            for key, val in obj.attrs.items():
                self.__sendOutput(' ' * n + "%s: %s" % (key, val), head='')
            self.__sendOutput(' ', head='')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    FileBrowser(subprocess=False).start()
